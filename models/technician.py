from tortoise.models import Model
from tortoise import fields


class TechnicianInfo(Model):
    __tablename__ = 'technicians'
    technician_id = fields.IntField(max_length=8, unique=True, pk=True)
    firstname = fields.CharField(max_length=50, null=False, help_text="Enter technician's firstname")
    lastname = fields.CharField(max_length=50, null=False, help_text="Enter technician's lastname")
    email_addr = fields.CharField(max_length=100, null=False, help_text="Enter technician's email address")
    phone_num = fields.CharField(max_length=20, null=False, help_text="Enter technician's phone number")
    certification_status = fields.CharField(max_length=20, choices=[("certified", "Certified"), ("pending", "Pending")], default="pending")
    EXPERIENCE_LEVEL_CHOICES = [
        ("Beginner"),
        ("Intermediate"),
        ("Advanced"),
        ("Expert")] 
    experience_level = fields.CharField(max_length=50, null=False, choices=EXPERIENCE_LEVEL_CHOICES, help_text="Select the technician's level of experience")
    specialization = fields.CharField(max_length=100, null=False, help_text="Enter technician's area of expertise/specialization")
    address = fields.TextField(null=False, help_text="Enter technician's complete address")
    certified = fields.BooleanField(default=False)
    notes = fields.TextField(null=True, help_text="Add any additional notes or comments related to the vehicle(optional)")
    actions = fields.CharField(max_length=100) 