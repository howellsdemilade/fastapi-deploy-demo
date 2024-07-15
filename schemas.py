from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Customer schemas
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email_addr: EmailStr
    phone_num: str
    address: str
    password: Optional[str] = None
    actions: Optional[str] = None
    last_service_date: Optional[date] = None
    additional_details: Optional[str] = None
    profile_picture: Optional[bytes] = None
    # created_at: Optional[date] = None

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_addr: Optional[EmailStr] = None
    phone_num: Optional[str] = None
    password: Optional[str] = None 
    address: Optional[str] = None
    actions: Optional[str] = None
    last_service_date: Optional[date] = None
    additional_details: Optional[str] = None
    profile_picture: Optional[bytes] = None
    # created_at: Optional[date] = None

# Vehicle schemas
class VehicleCreate(BaseModel):
    customer_id: int
    make: str
    model: str
    year: int
    registration_num: str
    vin: Optional[str] = None
    license_num: str
    color: Optional[str] = None
    mileage: Optional[int] = None
    insurance_company: Optional[str] = None
    policy_num: Optional[str] = None
    policy_start_date: Optional[date]= None
    policy_end_date: Optional[date] = None
    notes: Optional[str] = None
    last_service_date: Optional[date] = None

class VehicleUpdate(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    registration_num: Optional[str]
    vin: Optional[str]
    license_num: Optional[str]
    color: Optional[str] = None
    mileage: Optional[int] = None
    insurance_company: Optional[str] = None
    policy_num: Optional[str] = None 
    policy_start_date: Optional[date] = None
    policy_end_date: Optional[date] = None
    notes: Optional[str] = None
    last_service_date: Optional[date] = None
    
class VehicleImage(BaseModel):
    vehicle_id: int
    image_data: bytes

class VehicleImageOut(BaseModel): 
    image: bytes
    
    
class CreateTechnician(BaseModel):
    firstname: str
    lastname: str
    email_addr: EmailStr
    phone_num: str
    certification_status: str
    experience_level: str
    specialization: str
    address: str
    certified: bool = False
    notes: Optional[str] = None
    actions: Optional[str] = None
    
class UpdateTechnician(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email_addr: Optional[EmailStr] = None
    phone_num: Optional[str] = None
    certification_status: Optional[str] = None
    experience_level: Optional[str] = None
    specialization: Optional[str] = None
    address: Optional[str] = None
    certified: Optional[bool] = None
    notes: Optional[str] = None
    actions: Optional[str] = None
    
    
# class CreateService(BaseModel):
    

    