from fastapi import APIRouter
from app.schemas.tasks import addTask
from app.schemas.tasks import updateTask

router = APIRouter()

tasks=[]


@router.get("/alltasks")
async def getAllTasks():
    return {"tasks": tasks}

#tasks by id
@router.get("/task/{task_id}")
async def getTaskById(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return {"task": task}
    return {"error": "Task not found"}


#add new task
@router.post("/addtask")
async def addTask(task: addTask):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

@router.put("/updatetask/{task_id}")
async def updateTask(id: int, Task: updateTask):
    for task in tasks:
        if task["id"] == id:
            if Task.title is not None:
                task["title"] = Task.title
            if Task.description is not None:
                task["description"] = Task.description
            if Task.completed is not None:
                task["completed"] = Task.completed
            return {"message": "Task updated successfully", "task": task}