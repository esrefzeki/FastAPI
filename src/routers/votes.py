from fastapi import Response, status, HTTPException, Depends, APIRouter
from FastAPI.src.api.models.dto import vote_dto
from FastAPI.src.api.models import models
from sqlalchemy.orm import Session
from FastAPI.src.api.infrastructure.persistance.db_manager import get_db
from FastAPI.src.security import oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Post Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votes: vote_dto.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {votes.post_id} does not exist.")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id,
                                               models.Votes.user_id == current_user.id)

    found_vote = vote_query.first()

    if votes.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {votes.post_id}")

        new_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
