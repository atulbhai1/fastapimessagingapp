from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func, or_
router = APIRouter(prefix="/posts", tags=["Posts"])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int=10, skip:int=0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(or_(models.Post.title.contains(search), models.Post.content.contains(search))).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def createposts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model= schemas.PostOut)
def get_latest_post(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at.desc()).first()
    return post

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    #val = cursor.fetchone()
    val = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not val:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID {id} Was Not Found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message", f"Post with id {id} was not found"}
    return val

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user:models.User= Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID {id} Was Not Found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO PREFORM ACTION")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #new_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID {id} Was Not Found")
    if old_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO PREFORM ACTION")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
