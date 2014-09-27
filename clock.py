from app import scripts
import worker
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

sched = BlockingScheduler()
queue = Queue(connection=worker.conn)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=16)
def cron_send_messages():
    result = queue.enqueue(scripts.cron.run)

@sched.scheduled_job('interval', minutes=3)
def cron_send_messages():
    result = queue.enqueue(scripts.cron.test)

sched.start()
