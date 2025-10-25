from fastapi import FastAPI #importing fastapi
from fastapi.middleware.cors import CORSMiddleware
from random import randrange
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

#print(settings.database_usernm)

#models.Base.metadata.create_all(bind = engine)  #No need of this code because of alembic

app = FastAPI()

#here main postgre connecting ocde is placed 

#my_posts = [{"title": "Title of post 1", "conent": "Content of post 1", "id": 1},{"title": "Title of post 2", "conent": "Content of post 2", "id": 2}]

'''
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i     
'''

origins = ["*"] #list of domains --["https://www.google.com", "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_method = ["*"] ,
    allow_headers = ["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #path define ("/login") 
async def root():
    return {"Message": "Hello World",
            "Message2": "Welcome to API's"}


'''
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    #1st query using python

    posts = db.query(models.Post).all()

    return { "data": posts}
'''


