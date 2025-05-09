from app.models.dbModels.EntityDB import EntityDB
from sqlalchemy import Column, String, UUID, DateTime, Integer
from sqlalchemy.orm import relationship


class UserEntity(EntityDB):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    predictions = relationship("PredictionEntity", back_populates="user", cascade="all, delete-orphan",
                               passive_deletes=True)

    def __init__(self, id=None, first_name=None, last_name=None, email=None, hashed_password=None, birth_date=None,
                 gender=None,
                 created_at=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password
        self.birth_date = birth_date
        self.gender = gender
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "created_at": self.created_at
        }
