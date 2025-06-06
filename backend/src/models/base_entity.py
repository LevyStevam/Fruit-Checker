from sqlalchemy import Column, String

class BaseEntity:
    created_at = Column(String)
    updated_at = Column(String) 