from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class EmailBase(BaseModel):
    sender: str
    subject: str
    body: str
    timestamp: Optional[datetime] = None
    is_read: bool = False
    category: str = "Uncategorized"
    action_items: str = "[]"

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    class Config:
        orm_mode = True

class PromptBase(BaseModel):
    name: str
    template_content: str
    description: Optional[str] = None

class PromptCreate(PromptBase):
    pass

class Prompt(PromptBase):
    id: int
    class Config:
        orm_mode = True

class DraftBase(BaseModel):
    email_id: int
    subject: str
    body: str
    status: str = "draft"

class DraftCreate(DraftBase):
    pass

class Draft(DraftBase):
    id: int
    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    email_id: int
    query: str

class ChatResponse(BaseModel):
    response: str
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
