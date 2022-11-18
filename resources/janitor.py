from models import *
import time
import werkzeug
import os
max_task_time = float(os.getenv('MAX_TASK_TIME'))

def RunTaskCleaner():
    print("[janitor] started janitor", flush=True)
    while 1:
        ts_current = time.time()
        
        task = Task.query.with_for_update(of=Task).filter(Task.created < ts_current-max_task_time).first()
        if task != None:
            print(f"[janitor] task {task.id} deleted because it exceeded max storage time", flush=True)
            Task.query.filter_by(id = task.id).delete()
            db.session.commit()