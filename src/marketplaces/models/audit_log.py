from pydantic import BaseModel
from datetime import datetime

class AuditLog(BaseModel):
    id: str
        user: str
            action: str
                details: str
                    timestamp: datetime
    