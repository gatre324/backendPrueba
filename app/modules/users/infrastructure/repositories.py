from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.infrastructure.models import UserModel


class SqlAlchemyUserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> UserModel | None:
        return self.db.scalar(select(UserModel).where(UserModel.email == email))

    def get_by_id(self, user_id: UUID) -> UserModel | None:
        return self.db.get(UserModel, user_id)

    def create(self, **values: object) -> UserModel:
        user = UserModel(**values)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
