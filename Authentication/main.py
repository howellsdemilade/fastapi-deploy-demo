import os
import jwt
import datetime
import Authentication.schemas as schemas
from dotenv import load_dotenv
from models.auth import User, TokenTable
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from Authentication.auth_bearer import JWTBearer
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, Depends, HTTPException, status
from Authentication.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password, create_password_reset_token, send_password_reset_email


app = FastAPI()

load_dotenv()

secret_key = os.getenv("JWT_SECRET_KEY")
secret_refresh_key = os.getenv("JWT_REFRESH_SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"



@app.get("/")
async def ping():
    return {
        "message": "API IS WORKING !!"
    }

@app.post("/signup", response_model=schemas.SignupResponse)
async def signup(request: schemas.SignupDetails):
    user = await User.get_or_none(email=request.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!")
    
    hashed_password = get_hashed_password(request.password)
    await User.create(email=request.email, password=hashed_password)
    
    return {
        "message": "Signup Successful!!"
    }


@app.post("/login", response_model=schemas.TokenSchema)
async def login(request: schemas.logindetails):
    user = await User.get_or_none(email=request.email)
    if user is None or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Credentials!") 
    
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    
    async with in_transaction() as conn:
        await TokenTable.create(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    
    return {
        "message": "Login Successfull!!",
        "access_token": access,
        "refresh_token": refresh,
    }


@app.post('/change-password')
async def changepassword(request: schemas.changepassword):
    try:
        user = await User.get(email=request.email)
    except DoesNotExist: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    await user.save()
    return {"message": "Password changed successfully"}



@app.post('/forgot-password')
async def forgot_password(request: schemas.ForgotPasswordRequest):
    try:
        user = await User.get(email=request.email)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    token = create_password_reset_token(user.email)
    send_password_reset_email(user.email, token)
    return {"message": "Password reset email sent"}



@app.post('/reset-password')
async def reset_password(request: schemas.ResetPasswordRequest):
    try: 
        payload = jwt.decode(request.token, secret_key, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    try:
        user = await User.get(email=email)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user.password = get_hashed_password(request.new_password)
    await user.save()
    return {"message": "Password reset successfully"}



@app.post('/logout')
async def logout(token: str = Depends(JWTBearer())):
    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    user_id = payload['sub']
    async with in_transaction() as conn:
        token_records = await TokenTable.filter(user_id=user_id).all()
        info = [record.user_id for record in token_records if (datetime.datetime.utcnow() - record.created_date).days > 1]
        
        if info:
            await TokenTable.filter(user_id__in=info).delete()
        
        existing_token = await TokenTable.filter(user_id=user_id, access_token=token).first()
        if existing_token:
            existing_token.status = False
            await existing_token.save()

    return {"message": "Logout Successfully"}


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




