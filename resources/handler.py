from models import *
import time
import werkzeug
import os
max_task_time = float(os.getenv('MAX_TASK_TIME'))

def ExecuteWhenRunningTask(task_id, args):
    return "none"

def RunTask(task_id, args):
    print(f"[handler] task {task_id} is running", flush=True)

    #do some logic here
    result_of_execution = ExecuteWhenRunningTask(task_id, args)

    return {"message": result_of_execution}

def TaskHandler():
    print("[handler] started taskhandler", flush=True)

    while 1:
        task = Task.query.with_for_update(of=Task).filter_by(status='waiting').first()
        if task != None:
            print(f'[handler] task {task.id} is ready to run.', flush=True)

            task.status = "running"
            db.session.commit()

            try:
                task.result = RunTask(task_id=task.id, args=task.args)
                print(f"[handler] task {task.id} is finished", flush=True)
                task.status = "done"
                db.session.commit()
            except:
                print(f"[handler] task {task.id} failed to run", flush=True)
                task.status = "waiting"
                db.session.commit()
    

           