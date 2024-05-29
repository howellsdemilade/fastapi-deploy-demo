from tortoise.models import Model
from tortoise import fields
from models.vehicle import VehicleInfo


class CustomerInfo(Model):
    __tablename__ = 'customers'
    customer_id = fields.CharField(max_length=6, unique=True)

    @classmethod
    async def generate_customer_id(cls):
        last_customer = await cls.all().order_by("-id").first()
        if last_customer:
            last_id = int(last_customer.customer_id[3:])  # Extract the number part
            new_id = last_id + 1
            return f"CUS{new_id:03d}"
        else:
            return "CUS001"  # If no previous customer, start from CUS001
    async def save(self, *args, **kwargs):
        if not self.customer_id:
            self.customer_id = await self.generate_customer_id()
        await super().save(*args, **kwargs)
    first_name = fields.CharField(max_length=50, null=False, help_text="Enter customer's firstname")
    last_name = fields.CharField(max_length=50, null=False, help_text="Enter customer's lastname")
    email_addr = fields.CharField(max_length=100, null=False, help_text="Enter customer's email address")
    last_service_date = fields.DateField(null=True, input_formats=["%Y-%m-%d"])
    actions = fields.CharField(max_length=100)
    phone_num = fields.CharField(max_length=20, null=False, help_text="Enter customer's phone number")
    address = fields.TextField(null=False, help_text="Enter customer's complete address")
    vehicles = fields.ReverseRelation["VehicleInfo"]    
    additional_details = fields.TextField(null=True, help_text="Additional notes")
    password = fields.CharField(max_length=255, null=False, help_text="............")
    profile_picture = fields.BinaryField(null=True)

