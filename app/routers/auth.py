from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import database, models, schema, utils
from . import auth2

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials!!!!")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials!!!!")
    
    #Create token
    access_token = auth2.create_access_token(data = {"user_id": user.id})
    
    #Return 
    return {"access_Token": access_token, "Token_type": "Bearer"}