from sqlalchemy.orm import Session
from src.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, nome: str):
        existing_user = self.db.query(User).filter(User.email == email).first()

        if existing_user:
            raise ValueError("Email ja cadastrado")

        user = User(email=email, nome=nome)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
