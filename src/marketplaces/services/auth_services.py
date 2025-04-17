from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.models.user import User, Role

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy users store
users_db = {
    "admin": User(id="1", username="admin", hashed_password=pwd_context.hash("admin123"), role=Role.ADMIN),
        "staff": User(id="2", username="staff", hashed_password=pwd_context.hash("staff123"), role=Role.STAFF),
        }

        def authenticate_user(username: str, password: str):
            user = users_db.get(username)
                if not user or not pwd_context.verify(password, user.hashed_password):
                        return None
                            return user

                            def create_access_token(user: User):
                                to_encode = {"sub": user.username, "role": user.role.value}
                                    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                                        to_encode.update({"exp": expire})
                                            return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

                                            def get_current_user(token: str) -> User:
                                                try:
                                                        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                                                                username = payload.get("sub")
                                                                        role = payload.get("role")
                                                                                return users_db.get(username)
                                                                                    except JWTError:
                                                                                            return None
                                                