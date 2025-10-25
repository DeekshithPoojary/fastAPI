from fastapi import FastAPI, Response, status, HTTPException ,Depends, APIRouter #importing fastapi
from .. import models, schema
from . import  auth2
from typing import List, Optional
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags = ['post']
)


#get all posts
#@router.get("/", response_model=List[schema.Post]) 
@router.get("/", response_model=List[schema.PostOut]) 
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user), limit: int = 50, skip: int = 0, search: Optional[str] = ""):

   # cursor.execute("""SELECT * FROM posts """)
   # posts = cursor.fetchall()
   # print(posts)
  # print("Post displaying limit is ", limit)
   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()  #here add offset after the limit for the skip funtion, in postman posts?limit&skip=2
                                            # models.Post.owner_id == current_user.id -- for authentication purpose
    
    

    #SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.create_at AS posts_create_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS "Votes"
    #FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id

    #join operations using sql alchemy - The top sql code is written like this using sqlalchemy

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    #print(results)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)   #@app.post("/createposts") instead of this we have to write like this ("/posts")
async def create_posts(post: schema.postCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):  #(payload: dict = Body(...))
    #print(post.rating)
    #print(post.dict())
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 100000)
    #my_posts.append(post.dict())
    #return {"Message": "Post method", "data": post}

    #cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) returning * """,
                 #   (post.title, post.content, post.published )) 
    #new_post = cursor.fetchone()

    #conn.commit()
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)

    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

'''
#Order matters, if this is written  below, then you will get an error.
@router.get("/posts/latestpost")
def get_latest_post():
    post = my_posts[len(my_posts) -1]
    return {"detail": post}
'''

#get one post

@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    #print(id)
    #cursor.execute(""" select * from posts where id = %s """, (str(id),))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail =  f"Post with is {id} was not found!!!"
                            )
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Message": f"Post with is {id} was not found!!!"}

    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform to requeted action!!!!")
    
    return post


#Delete a request

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  #status code must be 4 while delete operation
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    #Delete post
    #find the index in the array that has required id
    #my_posts.pop(index)

    #cursor.execute(""" delete from posts where id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post =  deleted_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Path is with {id} does not exist!!")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform to requeted action!!!!")
    
    deleted_post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.postCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    #cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    updating_post = db.query(models.Post).filter(models.Post.id == id)

    if updating_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Path is with {id} does not exist!!")
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict

    if updating_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform to requeted action!!!!")

    updating_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updating_post.first()