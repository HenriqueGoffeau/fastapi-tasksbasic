from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = None
    
    class Config:
        from_attributes = True
        
class TaskCreate(TaskBase):
    class Config:
        from_attributes = True