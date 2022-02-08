from pydantic import BaseModel
from datetime import datetime
from FastAPI.src.api.models.dto.users_dto import UserResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime = datetime.now()
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True  # Pydantic modeller dict ile çalıştığı için sqlalchemy modellerinden ziyade bunları dict olarak ister
