from tortoise.models import Model
from tortoise import fields
from models.vehicle import VehicleInfo

class Invoice(Model):
    __tablename__ = 'invoices'
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]
    id = fields.IntField(max_length=6, unique=True, pk=True)

    service = fields.ForeignKeyField('models.ServiceLog', related_name='invoices')

    paid_status = fields.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_amount_paid = fields.DecimalField(max_digits=10, decimal_places=2)
    service_description = fields.CharField(max_length=200, help_text="Additional service details or notes")
    service_amount = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Enter amount charged for the service")
    
    async def populate_customer_details(self):
        if self.customer:
            self.customer_name = self.customer.customer_name
            self.customer_email = self.customer.email
            self.customer_phone_number = self.customer.phone_number
            self.customer_address = self.customer.address

    async def populate_vehicle_details(self):
        if self.vehicle:
            vehicle_info = await VehicleInfo.filter(id=self.vehicle.id).first()
            if vehicle_info:
                self.vehicle_make = vehicle_info.make
                self.vehicle_model = vehicle_info.model
                self.vehicle_license_plate = vehicle_info.license_num
                self.vehicle_vin = vehicle_info.vin












# from tortoise import Model, fields
# from models import VehicleInfo, CustomerInfo


# class Invoice(Model):
#     STATUS_CHOICES = [
#         ('paid', 'Paid'),
#         ('pending', 'Pending'),
#     ]
#     invoice_id = fields.CharField(max_length=10, unique=True)

#     customer = fields.ForeignKeyField('models.CustomerInfo', related_name='invoices')
#     vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='invoices')
    
#     vehicle_make = fields.CharField(max_length=50, null=False, help_text="Auto-based field based on the selected vehicle ID")
#     vehicle_model = fields.CharField(max_length=50, null=False, help_text="Auto-based field based on the selected vehicle ID")
#     vehicle_license_plate = fields.CharField(max_length=20, null=False, help_text="Auto-based field based on the selected vehicle ID")
#     vehicle_vin = fields.CharField(max_length=20, null=False, help_text="Auto-based field based on the selected vehicle ID")
    
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
    
#     service_type = fields.ChoiceField(choices=SERVICE_TYPES, help_text="Select service type")
#     paid_status = fields.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     total_amount_paid = fields.DecimalField(max_digits=10, decimal_places=2)
#     service_date = fields.DateField(help_text="Select the date of the service appointment")
#     service_description = fields.CharField(max_length=200, help_text="Additional service details or notes")
#     service_amount = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Enter amount charged for the service")
#     async def save(self, *args, **kwargs):
#         if not self.invoice_id:
#             last_invoice = await Invoice.all().order_by('-id').first()
#             if last_invoice:
#                 last_id = int(last_invoice.invoice_id[3:])  # Extract the numeric part
#                 self.invoice_id = f"INV{last_id + 1:03d}"
#             else:
#                 self.invoice_id = "INV001"
#         await super().save(*args, **kwargs)
    
#     async def populate_customer_details(self):
#         if self.customer:
#             self.customer_name = self.customer.customer_name
#             self.customer_email = self.customer.email
#             self.customer_phone_number = self.customer.phone_number
#             self.customer_address = self.customer.address

#     async def populate_vehicle_details(self):
#         if self.vehicle:
#             vehicle_info = await VehicleInfo.filter(id=self.vehicle.id).first()
#             if vehicle_info:
#                 self.vehicle_make = vehicle_info.make
#                 self.vehicle_model = vehicle_info.model
#                 self.vehicle_license_plate = vehicle_info.license_num
#                 self.vehicle_vin = vehicle_info.vin
#     actions = fields.CharField(max_length=100)
#     total_amount = fields.DecimalField(max_digits=20, decimal_places=3, null=True)
# # class Invoice(Model):
# #     customer = fields.ForeignKeyField('models.CustomerInfo', related_name='invoices')
# #     customer_id = fields.IntField(help_text="Select the customer ID from the list of registered customers", null=False)
    
# #     vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='invoices')
# #     vehicle_id = fields.IntField(help_text="Select the vehicle ID from the list of registered vehicles", null=False)
# #     vehicle_make = fields.CharField(max_length=50, null=False, help_text="Auto-based field based on the selected vehicle ID")
# #     vehicle_model = fields.CharField(max_length=50, null=False, help_text="Auto-based field based on the selected vehicle ID")
# #     vehicle_license_plate = fields.CharField(max_length=20, null=False, help_text="Auto-based field based on the selected vehicle ID")
# #     vehicle_vin = fields.CharField(max_length=20, null=False, help_text="Auto-based field based on the selected vehicle ID")
# #     SERVICE_TYPES = [
# #         ("Maintenance"),
# #         ("Repair"),
# #         ("Customization"),
# #         ("Inspection"),
# #         ("Oil Change"),
# #         ("Tire Rotation"),
# #         ("Brake Service"),
# #         ("Engine Tune-up"),
# #         ("Diagnostics"),
# #         ("Electrical Work"),
# #     ]
    
# #     service_type = fields.ChoiceField(choices=SERVICE_TYPES, help_text="Select service type")
# #     service_date = fields.DateField(help_text="Select the date of the service appointment")
# #     service_description = fields.CharField(max_length=200, help_text="Additional service details or notes")
# #     service_amount = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Enter amount charged for the service")
    
# #     async def populate_customer_details(self):
# #         if self.customer:
# #             self.customer_name = self.customer.customer_name
# #             self.customer_email = self.customer.email
# #             self.customer_phone_number = self.customer.phone_number
# #             self.customer_address = self.customer.address

# #     async def populate_vehicle_details(self):
# #         if self.vehicle_id:
# #             vehicle_info = await VehicleInfo.filter(id=self.vehicle_id).first()
# #             if vehicle_info:
# #                 self.vehicle_make = vehicle_info.make
# #                 self.vehicle_model = vehicle_info.model
# #                 self.vehicle_license_plate = vehicle_info.license_plate
# #                 self.vehicle_vin = vehicle_info.vin
# #     @property
# #     def customer_name(self):
# #         return self.customer.customer_name if self.customer else None

# #     @property
# #     def customer_email(self):
# #         return self.customer.email if self.customer else None

# #     @property
# #     def customer_phone_number(self):
# #         return self.customer.phone_number if self.customer else None

# #     @property
# #     def customer_address(self):
# #         return self.customer.address if self.customer else None
    