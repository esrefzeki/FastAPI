from fastapi import Response, status, HTTPException, Depends, APIRouter
from FastAPI.src.api.models.dto import vote_dto
from sqlalchemy.orm import Session
from FastAPI.src.api.infrastructure.persistance.db_manager import get_db
from FastAPI.src.security import oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Post Votes"]
)

router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: vote_dto.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(vote_dto.Vote).filter(vote_dto.Vote.post_id == vote.post_id,
                                                vote_dto.Vote.user)