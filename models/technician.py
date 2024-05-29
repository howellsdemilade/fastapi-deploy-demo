from tortoise.models import Model
from tortoise import fields


class TechnicianInfo(Model):
    __tablename__ = 'technicians'
    technician_id = fields.CharField(max_length=8, unique=True)

    @classmethod
    async def get_last_technician_number(cls):
        last_technician = await cls.all().order_by("-id").first()
        if last_technician:
            last_number = int(last_technician.technician_id[4:])  # Extract the number part
            return last_number
        return 0  # If no previous technician exists, start from 0

    async def generate_technician_id(self):
        last_number = await self.get_last_technician_number()
        new_number = last_number + 1
        return f"TECH{new_number:03d}"

    async def save(self, *args, **kwargs):
        if not self.technician_id:
            self.technician_id = await self.generate_technician_id()
        await super().save(*args, **kwargs)
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