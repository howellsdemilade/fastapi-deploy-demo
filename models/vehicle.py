
from datetime import datetime
from tortoise.models import Model
from tortoise import fields

class VehicleInfo(Model):
    __tablename__ = 'vehicles'
    vehicle_id = fields.CharField(max_length=6, unique=True)
    @classmethod
    async def get_last_vehicle_number(cls):
        last_vehicle = await cls.all().order_by("-id").first()
        if last_vehicle:
            last_number = int(last_vehicle.vehicle_id[3:])  # Extract the number part
            return last_number
        return "VEH001"  # If no previous vehicle exists, start from 0

    async def generate_vehicle_id(self):
        last_number = await self.get_last_vehicle_number()
        new_number = last_number + 1
        return f"VEH{new_number:03d}"


    async def save(self, *args, **kwargs):
        if not self.vehicle_id:
            self.vehicle_id = await self.generate_vehicle_id()

    customer = fields.ForeignKeyField('models.CustomerInfo', related_name='vehicle')
    make = fields.CharField(max_length=50, null=False, help_text="Enter the make of your vehicle")
    model = fields.CharField(max_length=50, null=False, help_text="Specify the model of the vehicle(e.g. Corolla, Civic, Mustang)")
    year_choices = [(year, str(year)) for year in range(datetime.now().year, 1900, -1)]
    year = fields.IntField(choices=year_choices, help_text="Select the manufacturing year of the vehicle")
    registration_num = fields.CharField(max_length=20, null=False, help_text="Input the registration number of the vehicle")
    last_service_date = fields.DateField(null=True, input_formats=["%Y-%m-%d"])
    actions = fields.CharField(max_length=100)

    vin = fields.CharField(max_length=20, null=False, help_text="Enter the vehicle VIN")
    license_num = fields.CharField(max_length=20, null=False, help_text="Input the license plate number of the vehicle")
    CAR_COLORS = [
        ("Black","BLACK"),("White", "WHITE"),("Silver","SILVER"),("Gray","GRAY"),("Red","RED"),("Blue","BLUE"),("Green","GREEN"),("Yellow","YELLOW"),("Orange","ORANGE"),("Purple","PURPLE"),("Brown","BROWN"),("Beige","BEIGE"),("Other")]
    color = fields.CharField(max_length=20, null=False, choices=CAR_COLORS, help_text="Specify the color of the vehicle")
    mileage = fields.IntField(null=False, help_text="Enter the correct mileage of the vehicle(in kilometers or miles)")
    insurance_company = fields.CharField(max_length=50, null=False, help_text="Enter name of the insurance company")
    policy_num = fields.CharField(max_length=20, null=False, help_text="e.g. POL123456")
    policy_start_date = fields.DateField(null=False, input_formats=["%m/%d/%y"], default=datetime.now().date(), help_text="mm/dd/yy")
    policy_end_date = fields.DateField(null=False, input_formats=["%m/%d/%y"], help_text="mm/dd/yy")
    notes = fields.TextField(null=True, help_text="Add any additional notes or comments related to the vehicle(optional)")


class VehicleImage(Model):
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='images')
    image = fields.BinaryField()

    class Meta:
        table = "vehicle_images"











 
    