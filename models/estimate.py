from tortoise.models import Model
from tortoise import fields
from models.vehicle import VehicleInfo
from models.customer import CustomerInfo



class EstimateItem(Model):
    __tablename__ = 'estimate_items'
    id = fields.IntField(pk=True)
    estimate_report = fields.ForeignKeyField('models.EstimateReport', related_name='items')
    item = fields.CharField(max_length=100, help_text="Enter item name")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, help_text="Enter item amount")

class EstimateReport(Model):
    __tablename__ = 'estimate'
    id = fields.IntField(max_length=6, unique=True, pk=True)
    
    # ForeignKeyField to VehicleInfo model
    vehicle = fields.ForeignKeyField('models.VehicleInfo', related_name='estimate_reports', null=False)

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('pending', 'Pending'),
    ]
    status = fields.CharField(max_length=10, choices=STATUS_CHOICES)
    actions = fields.CharField(max_length=100)
    date = fields.DateField() 

    async def populate_customer_vehicle_details(self):
        if self.customer_id:
            customer = await CustomerInfo.filter(id=self.customer_id).first()
            if customer:
                self.customer = customer
        
        if self.vehicle_id:
            vehicle = await VehicleInfo.filter(id=self.vehicle_id).first()
            if vehicle:
                self.vehicle = vehicle
