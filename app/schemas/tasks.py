from pydantic import BaseModel


#Lazem dir wahda lkoul task
class addTask(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False



class updateTask(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None