from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session
router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User=Depends(oauth2.get_current_user)):
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With Id {vote.post_id} was not found")
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id,
                                              models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User: {current_user.id} Has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"You voted on post {vote.post_id}"}
    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VOTE DOES NOT EXIST")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Deleted Vote on post {vote.post_id}"}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='"dir" cannot be anything other than 1 or 0')