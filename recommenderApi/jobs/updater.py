# from apscheduler.schedulers.background import BackgroundScheduler
# from jobs.jobs import schedule, dt
# from recommenderApi.settings import HOUR, MINUTE

# def start():
# 	scheduler = BackgroundScheduler(timezone='Egypt')
# 	schedular = schedule(dt.now())
# 	print(f'Scheduled at: {HOUR} {MINUTE}')
# 	scheduler.add_job(schedular.schedule_job, 'cron', hour=HOUR, minute=MINUTE)
# 	scheduler.start()