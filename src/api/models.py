from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    fullname: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=True, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "isActive": self.is_active
            # do not serialize the password, its a security breach
        }

# Se agregó un modelo para guardar los tokens bloqueados por cierres de sesión


class TokenBlocklist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(String(50), nullable=False)
