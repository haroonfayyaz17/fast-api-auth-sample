import bcrypt
from sqlalchemy import event, Column, Integer, String
from sqlalchemy.orm import Session
from app.database import Base, engine

# Define To Do class inheriting from Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(256), unique=True)
    password = Column(String(256))

    @classmethod
    def hash_password(self, password):
        bytes = password.encode('utf-8')

        # Hashing the password
        hash = bcrypt.hashpw(bytes, salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    @classmethod
    def is_password_valid(self, password, hash):
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

    @classmethod
    def authenticate(self, email, password):
        db = Session(bind=engine, expire_on_commit=False)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return "User with this email doesn't exist"

        if not self.is_password_valid(password, user.password):
            return "Password doesn't match"

        return user


@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.password = User.hash_password(target.password)

