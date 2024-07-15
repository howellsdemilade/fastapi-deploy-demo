from tortoise.models import Model
from tortoise import fields


class ServiceLog(Model):
    __tablename__ = 'services'
    id = fields.IntField(max_length=6, unique=True, pk=True)
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='services', to_field='id', db_constraint=False)
    technician = fields.ForeignKeyField('models.TechnicianInfo', related_name='services', to_field='technician_id', db_constraint=False)    
    SERVICE_TYPES = [
        ("Maintenance", "Maintenance"),
        ("Repair", "Repair"),
        ("Customization", "Customization"),
        ("Inspection", "Inspection"),
        ("Oil Change", "Oil Change"),
        ("Tire Rotation", "Tire Rotation"),
        ("Brake Service", "Brake Service"),
        ("Engine Tune-up", "Engine Tune-up"),  
        ("Diagnostics", "Diagnostics"),
        ("Electrical Work", "Electrical Work"),
    ]
    service_type = fields.CharField(max_length=100, null=False, choices=SERVICE_TYPES, help_text="Select service type")
    time = fields.TimeField(null=False, help_text="Select appointment time")
    date = fields.DateField(null=False, help_text="Select appointment date")
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        # Add more status options as needed
    ]
    status = fields.CharField(max_length=50, null=True, choices=STATUS_CHOICES, help_text="Update status")
    comments = fields.TextField(null=True, help_text="Any feedback or comments")
    actions = fields.CharField(max_length=100)
    customer_name = fields.CharField(max_length=100, null=False)
