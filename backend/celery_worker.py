# from celery import Celery, Task
# from celery.schedules import crontab
# from app import app
# celery_app = Celery('tasks',broker='redis://localhost:6379/1',backend='redis://localhost:6379/2',include=['tasks'])




# class FlaskTask(Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)
    
# celery_app.Task = FlaskTask
# celery_app.conf.timezone = 'Asia/Kolkata'

# celery_app.conf.beat_schedule = {
#     'monthly-user-report':{
#         'task':'tasks.send_monthly_report',
#         'schedule':crontab(minute=54, hour=18, day_of_month=17),
        
#     },
#     'daily-reminder':{
#         'task':'tasks.send_daily_reminder',
#         'schedule':crontab(minute=48, hour=18),
        
#     }
#     # 'export':{
#     #     'task':'tasks.export(student_id)',
#     #     'schedule':crontab(minute=32, hour=23),
#     # }
# }



import os
from celery import Celery, Task
from celery.schedules import crontab
from app import app

redis_url = os.getenv("REDIS_URL")

if not redis_url:
    raise RuntimeError("REDIS_URL environment variable is missing")

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", redis_url),
    backend=os.getenv("CELERY_RESULT_BACKEND", redis_url),
    include=["tasks"]
)

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = FlaskTask

celery_app.conf.timezone = "Asia/Kolkata"

celery_app.conf.beat_schedule = {
    "monthly-user-report": {
        "task": "tasks.send_monthly_report",
        "schedule": crontab(
            minute=54,
            hour=18,
            day_of_month=17
        ),
    },
    "daily-reminder": {
        "task": "tasks.send_daily_reminder",
        "schedule": crontab(
            minute=48,
            hour=18
        ),
    }
}
