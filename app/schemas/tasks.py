from pydantic import BaseModel


#Lazem dir wahda lkoul task
class Task(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

