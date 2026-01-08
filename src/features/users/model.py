from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(nullable=False, default="User")
	email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

	tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

	def __repr__(self) -> str:
		return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
