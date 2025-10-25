from fastapi import FastAPI, Response, status, HTTPException ,Depends, APIRouter #importing fastapi
from .. import models, schema, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users",
    tags = ['post']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.userOut)
def create_user(user: schema.userCreate, db: Session = Depends(get_db)):

    print("pass R", user.password)
    print("Pass len", len(user.password))
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long — must be less than 72 characters."
        )


    #hash the password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model = schema.userOut)
def get_user(id: int, db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with {id} is not present!!!!")
    
    return user

