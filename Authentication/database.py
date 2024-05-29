import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

database_url = os.getenv("URL_DATABASE")

async def init():
    await Tortoise.init(
        db_url=database_url,
        modules={'models': [
            "models.VehicleInfo", 
            "models.customer", 
            "models.estimate", 
            "models.inspection", 
            "models.invoice", 
            "models.service", 
            "models.auth",
            "models.technician"
        ]}
    )
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections() 