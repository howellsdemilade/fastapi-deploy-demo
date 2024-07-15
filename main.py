import os
import logging
from datetime import datetime, timedelta
from typing import List
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from models.estimate import EstimateItem, EstimateReport 
from models.inspection import InspectionReport
from models.invoice import Invoice
from models.service import ServiceLog
from models.technician import TechnicianInfo
from models.customer import CustomerInfo
from models import messages
from models.vehicle import VehicleImage, VehicleInfo
from fastapi import FastAPI, HTTPException, UploadFile, File
from schemas import CustomerCreate, CustomerUpdate, VehicleCreate, VehicleUpdate, VehicleImageOut, CreateTechnician, UpdateTechnician

app = FastAPI()


# Define endpoints
@app.post("/customers/", response_model=CustomerCreate)
async def create_customer(customer: CustomerCreate):
    # Create a new customer record
    new_customer = await CustomerInfo.create(**customer.dict())
    return new_customer

@app.get("/customers/{customer_id}", response_model=CustomerCreate, responses={404: {"model": HTTPNotFoundError}})
async def read_customer(customer_id: int):
    # Retrieve a customer by customer_id
    customer = await CustomerInfo.filter(id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerCreate(**customer.__dict__)

@app.put("/customers/{customer_id}", response_model=CustomerUpdate, responses={404: {"model": HTTPNotFoundError}})
async def update_customer(customer_id: int, customer: CustomerUpdate):
    # Update a customer record
    await CustomerInfo.filter(id=customer_id).update(
        **customer.dict(exclude_unset=True, exclude_none=True)
    )
    updated_customer = await CustomerInfo.filter(id=customer_id).first()
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerUpdate(**updated_customer.__dict__)

@app.delete("/customers/{customer_id}", response_model=dict, responses={404: {"model": HTTPNotFoundError}})
async def delete_customer(customer_id: int):
    # Delete a customer record
    deleted_count = await CustomerInfo.filter(id=customer_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
 

@app.get("/customers-total", response_model=dict)
async def get_total_customers():
    # Get total number of customers
    total_customers = await CustomerInfo.all().count()
    return {"total_customers": total_customers}

@app.get("/customers-last7days", response_model=dict)
async def get_customers_last_7_days():
    # Get number of customers created in the last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_customers = await CustomerInfo.filter(created_at__gte=seven_days_ago).count()
    return {"customers_last_7_days": recent_customers}

@app.post("/vehicles/", response_model=VehicleCreate)
async def create_vehicle(vehicle: VehicleCreate):
    # Check if customer exists
    customer = await CustomerInfo.filter(id=vehicle.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check if vehicle with the same registration number or VIN already exists
    existing_vehicle = await VehicleInfo.filter(registration_num=vehicle.registration_num).first()
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle with this registration number already exists")    
    vehicle_obj = VehicleInfo(**vehicle.dict(exclude_unset=True))
    vehicle_obj.customer_id = customer.id  # Tie vehicle to the existing customer
    await vehicle_obj.save()
    return vehicle 

@app.get("/vehicles/{vehicle_id}", response_model=VehicleCreate)
async def get_vehicle(vehicle_id: int):
    vehicle = await VehicleInfo.filter(id=vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.put("/vehicles/{vehicle_id}", response_model=VehicleCreate)
async def update_vehicle(vehicle_id: int, vehicle_update: VehicleUpdate):
    # Fetch the vehicle by its ID
    vehicle = await VehicleInfo.filter(id=vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Update vehicle attributes based on vehicle_update data
    if vehicle_update.make:
        vehicle.make = vehicle_update.make
    if vehicle_update.model:
        vehicle.model = vehicle_update.model
    # Save the changes to the database
    await vehicle.save()
    return vehicle

@app.delete("/vehicles/{vehicle_id}", response_model=dict)
async def delete_vehicle(vehicle_id: int):
    # Fetch the vehicle by its ID
    vehicle = await VehicleInfo.filter(id=vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    # Delete the vehicle from the database
    await vehicle.delete()
    return {"message": "Vehicle deleted successfully"}

@app.post("/vehicles/{vehicle_id}/images/", response_model=VehicleImageOut)
async def create_vehicle_image(vehicle_id: int, image: UploadFile = File(...)):
    vehicle = await VehicleInfo.get(id=vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    image = await image.read()
    # Assuming you have a model `VehicleImage` with fields `vehicle_id` and `image_data`
    vehicle_image = VehicleImage(vehicle_id=vehicle.id, image=image)
    await vehicle_image.save()

    return VehicleImageOut(image=image)

@app.get("/vehicles/{vehicle_id}/images/", response_model=List[VehicleImageOut])
async def get_vehicle_images(vehicle_id: int):
    vehicle = await VehicleInfo.get(id=vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    # Fetch all images associated with the vehicle
    images = await VehicleImage.filter(vehicle_id=vehicle.id)
    # Return a list of image data wrapped in VehicleImageOut objects
    return [VehicleImageOut(image=image.image_data) for image in images]

# Create Technician
@app.post("/technicians/", response_model=CreateTechnician)
async def create_technician(technician: CreateTechnician):
    async with in_transaction() as conn:
        new_technician = await TechnicianInfo.create(
            **technician.dict(exclude_unset=True, exclude_none=True)
        )
        return new_technician

# Read Technician
@app.get("/technicians/{technician_id}", response_model=CreateTechnician, responses={404: {"model": HTTPNotFoundError}})
async def read_technician(technician_id: int):
    technician = await TechnicianInfo.filter(technician_id=technician_id).first()
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    return CreateTechnician(
        firstname=technician.firstname,
        lastname=technician.lastname,
        email_addr=technician.email_addr,
        phone_num=technician.phone_num,
        certification_status=technician.certification_status,
        experience_level=technician.experience_level,
        specialization=technician.specialization,
        address=technician.address,
        certified=technician.certified,
        notes=technician.notes,
        actions=technician.actions
    )

# Update Technician
@app.put("/technicians/{technician_id}", response_model=CreateTechnician, responses={404: {"model": HTTPNotFoundError}})
async def update_technician(technician_id: int, technician_update: UpdateTechnician):
    async with in_transaction() as conn:
        updated_count = await TechnicianInfo.filter(technician_id=technician_id).update(
            **technician_update.dict(exclude_unset=True, exclude_none=True)
        )
        if not updated_count:
            raise HTTPException(status_code=404, detail="Technician not found")
        
        updated_technician = await TechnicianInfo.filter(technician_id=technician_id).first()
        return CreateTechnician(
            firstname=updated_technician.firstname,
            lastname=updated_technician.lastname,
            email_addr=updated_technician.email_addr,
            phone_num=updated_technician.phone_num,
            certification_status=updated_technician.certification_status,
            experience_level=updated_technician.experience_level,
            specialization=updated_technician.specialization,
            address=updated_technician.address,
            certified=updated_technician.certified,
            notes=updated_technician.notes,
            actions=updated_technician.actions
        )


# Delete Technician
@app.delete("/technicians/{technician_id}", response_model=dict, responses={404: {"model": HTTPNotFoundError}})
async def delete_technician(technician_id: int):
    deleted_count = await TechnicianInfo.filter(technician_id=technician_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Technician not found")
    return {"message": "Technician deleted successfully"}


TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("URL_DATABASE")
    },
    "apps": {
        "models": {
            "models": [
                "models.vehicle", 
                "models.customer",  
                "models.estimate", 
                "models.inspection",
                "models.invoice", 
                "models.service", 
                "models.technician", 
                "models.auth",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
print("Database URL:", os.getenv("URL_DATABASE"))

# Ensure the app runs correctly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)