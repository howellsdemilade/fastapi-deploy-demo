from tortoise.models import Model
from tortoise import fields

class CustomerInfo(Model):
    __tablename__ = 'customers'
    id = fields.IntField(pk=True)  # Auto-incrementing primary key
    first_name = fields.CharField(max_length=50, null=False, help_text="Enter customer's firstname")
    last_name = fields.CharField(max_length=50, null=False, help_text="Enter customer's lastname")
    email_addr = fields.CharField(max_length=100, null=False, unique=True, help_text="Enter customer's email address")
    last_service_date = fields.DateField(null=True, input_formats=["%Y-%m-%d"])
    actions = fields.CharField(max_length=100)
    phone_num = fields.CharField(max_length=20, null=False, help_text="Enter customer's phone number")
    address = fields.TextField(null=False, help_text="Enter customer's complete address")
    additional_details = fields.TextField(null=True, help_text="Additional notes")
    profile_picture = fields.BinaryField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


 