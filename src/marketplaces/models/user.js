from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
        STAFF = "staff"
            VIEWER = "viewer"

            class User(BaseModel):
                id: str
                    username: str
                        hashed_password: str
                            role: Role
                            