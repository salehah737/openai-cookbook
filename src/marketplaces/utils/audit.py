import uuid
from datetime import datetime
from src.models.audit_log import AuditLog

audit_logs = []

def log_action(user: str, action: str, details: str):
    entry = AuditLog(
            id=str(uuid.uuid4()),
                    user=user,
                            action=action,
                                    details=details,
                                            timestamp=datetime.utcnow()
                                                )
                                                    audit_logs.append(entry)
                                                        print(f"[AUDIT] {entry.timestamp} | {entry.user} | {entry.action} | {entry.details}")
    