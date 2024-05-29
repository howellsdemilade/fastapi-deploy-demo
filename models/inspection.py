from tortoise.models import Model
from tortoise import fields


class InspectionReport(Model):
    __tablename__ = 'inspection'
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='inspections')
    report_id = fields.CharField(max_length=8, unique=True)
    
    @classmethod
    async def get_last_report_number(cls):
        last_report = await cls.all().order_by("-id").first()
        if last_report:
            last_number = int(last_report.report_id[3:])  # Extract the number part
            return last_number
        return 0  # If no previous report exists, start from 0

    async def generate_report_id(self):
        last_number = await self.get_last_report_number()
        new_number = last_number + 1
        return f"REP{new_number:03d}"

    async def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = await self.generate_report_id()
        await super().save(*args, **kwargs)
    
    actions = fields.CharField(max_length=100)
    date = fields.DateField(null=False, input_formats=["%m/%d/%y"])

    inspector_choices = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Brown"]
    inspector = fields.CharField(max_length=100, help_text="Select inspector", choices=inspector_choices)
    inspection_date = fields.DateField(help_text="Select inspection date")
    inspection_note = fields.TextField(help_text="Inspection notes or comment")
    
    component = fields.CharField(max_length=100, help_text="Enter component checked")
    condition_choices = [
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    ] 
    condition = fields.CharField(max_length=100, help_text="Select the condition of the component", choices=condition_choices)
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]
    status = fields.CharField(max_length=20, choices=STATUS_CHOICES)

    async def populate_vehicle_details(self):
        if self.vehicle:
            self.customer_name = self.vehicle.customer_name
            self.vehicle_make = self.vehicle.make
            self.vehicle_model = self.vehicle.model
            self.vin = self.vehicle.vin
            self.license_num = self.vehicle.license_num


