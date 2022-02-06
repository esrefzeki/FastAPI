from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass
    # title: str
    # content: str
    # owner_id: int
    #
    # class Config:
    #     orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime = datetime.now()
    owner_id: int

    class Config:
        orm_mode = True  # Pydantic modeller dict ile çalıştığı için sqlalchemy modellerinden ziyade bunları dict olarak ister
