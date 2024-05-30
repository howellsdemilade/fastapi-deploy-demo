import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

database_url = os.getenv("URL_DATABASE")

async def init():
    try:
        await Tortoise.init(
            db_url=database_url,
            modules={'models': [
                "models.vehicle",
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
        print("Tortoise-ORM initialized and schemas generated successfully.")
    except Exception as e:
        print(f"Error initializing Tortoise-ORM: {e}")

async def close():
    try:
        await Tortoise.close_connections()
        print("Tortoise-ORM connections closed successfully.")
    except Exception as e:
        print(f"Error closing Tortoise-ORM connections: {e}")