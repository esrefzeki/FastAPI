from FastAPI.src.db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE") #default=True yerine kullanıyoruz çünkü server ile bağ kurmamız gerekiyor.
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))