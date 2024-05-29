from tortoise.models import Model
from tortoise import fields

    
class Message(Model):
    customer_id = fields.IntField(help_text="Select the customer ID from the list of registered customers", null=False)
    subject = fields.CharField(max_length=255, help_text="Enter the message title")
    body = fields.TextField(help_text="Enter your message body")
    
    
    @property
    def word_count(self):
        return len(self.body.split())

    def __str__(self):
        return self.subjec