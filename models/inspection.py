from tortoise.models import Model
from tortoise import fields


class InspectionReport(Model):
    __tablename__ = 'inspection'
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='inspections')
    id = fields.IntField(max_length=6, unique=True, pk=True)
    
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


