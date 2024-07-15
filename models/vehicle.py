from datetime import datetime
from tortoise.models import Model
from tortoise import fields

class VehicleInfo(Model):
    __tablename__ = 'vehicles'
    id = fields.IntField(max_length=6, unique=True, pk=True)
    customer = fields.ForeignKeyField('models.CustomerInfo', related_name='vehicle', to_field='id', db_constraint=False)
    make = fields.CharField(max_length=50, null=False, help_text="Enter the make of your vehicle")
    model = fields.CharField(max_length=50, null=False, help_text="Specify the model of the vehicle(e.g. Corolla, Civic, Mustang)")
    year_choices = [(year, str(year)) for year in range(datetime.now().year, 1900, -1)]
    year = fields.IntField(choices=year_choices, help_text="Select the manufacturing year of the vehicle")
    registration_num = fields.CharField(max_length=20, null=False, help_text="Input the registration number of the vehicle")
    last_service_date = fields.DateField(null=True, input_formats=["%Y-%m-%d"])

    vin = fields.CharField(max_length=20, null=True, help_text="Enter the vehicle VIN")
    license_num = fields.CharField(max_length=20, null=False, help_text="Input the license plate number of the vehicle")
    CAR_COLORS = [
        ("Black","BLACK"),("White", "WHITE"),("Silver","SILVER"),("Gray","GRAY"),("Red","RED"),("Blue","BLUE"),("Green","GREEN"),("Yellow","YELLOW"),("Orange","ORANGE"),("Purple","PURPLE"),("Brown","BROWN"),("Beige","BEIGE"),("Other")]
    color = fields.CharField(max_length=20, choices=CAR_COLORS, help_text="Specify the color of the vehicle", null=True)
    mileage = fields.IntField(help_text="Enter the correct mileage of the vehicle(in kilometers or miles)", null=True)
    insurance_company = fields.CharField(max_length=50, help_text="Enter name of the insurance company", null=True)
    policy_num = fields.CharField(max_length=20, help_text="e.g. POL123456", null=True)
    policy_start_date = fields.DateField( input_formats=["%m/%d/%y"], help_text="mm/dd/yy")
    policy_end_date = fields.DateField( input_formats=["%m/%d/%y"], help_text="mm/dd/yy")
    notes = fields.TextField( help_text="Add any additional notes or comments related to the vehicle(optional)")


class VehicleImage(Model):
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='images')
    image = fields.BinaryField()

    class Meta:
        table = "vehicle_images"

 