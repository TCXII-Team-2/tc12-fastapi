from fastapi import FastAPI
app= FastAPI()


tasks=[]

@app.get("/alltasks")
async def getAllTasks():
    return {"tasks": tasks}

#tasks by id
@app.get("/task/{task_id}")
async def getTaskById(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return {"task": task}
    return {"error": "Task not found"}


#add new task
@app.post("/addtask")
async def addTask(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}