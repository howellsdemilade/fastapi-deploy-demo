from tortoise.models import Model
from tortoise import fields


class ServiceLog(Model):
    __tablename__ = 'services'
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='services')
    technician = fields.ForeignKeyField('models.TechnicianInfo', related_name='services')    
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















# from tortoise import Model, fields

# class ServiceLog(Model):
#     vehicle_id = fields.IntField(null=False, help_text= "Enter vehicle ID")
#     vehicle_name = fields.CharField(max_length=100, null=False)
#     SERVICE_TYPES = [
#         ("Maintenance"),
#         ("Repair"),
#         ("Customization"),
#         ("Inspection"),
#         ("Oil Change"),
#         ("Tire Rotation"),
#         ("Brake Service"),
#         ("Engine Tune-up"), 
#         ("Diagnostics"),
#         ("Electrical Work"),
#     ]
#     technician = fields.CharField(max_length=100, null=False, help_text="Assign technician to the service by entering ID")
#     email_addr = fields.CharField(max_length=100, null=False, help_text="Enter technician's email address")

#     service_type = fields.CharField(max_length=100, null=False, choices=SERVICE_TYPES, help_text="Select service type")
#     time = fields.TimeField(null=False, help_text="Select appointment time")
#     date = fields.DateField(null=False, help_text="Select appointment date")
#     STATUS_CHOICES = [
#         ("Pending"),
#         ("In Progress"),
#         ("Completed"),
#         ("Cancelled"),
#         # Add more status options as needed
#     ]
#     status = fields.CharField(max_length=50, null=True, choices=STATUS_CHOICES, help_text="Update status")
#     FEEDBACK_CHOICES = [
#         ("Very Dissatisfied"),
#         ("Dissatisfied"),
#         ("Neutral"),
#         ("Satisfied"),
#         ("Very Satisfied")]
#     customer_feedback = fields.CharField(max_length=50, null=True, choices=FEEDBACK_CHOICES, help_text="Select feedback rated")
#     comments = fields.TextField(null=True, help_text="Any feedback or comments")
#     vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='services')
#     actions = fields.CharField(max_length=100)

#     customer_id = fields.IntField(null=False, help_text="Enter customer's ID")
    
    
#     customer_name = fields.CharField(max_length=100, null=False)
