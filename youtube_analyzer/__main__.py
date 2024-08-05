import os

from apscheduler.schedulers.blocking import BlockingScheduler

from youtube_analyzer.main import main

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(main, "cron", hour="8-21", minute="15", max_instances=1)
    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
