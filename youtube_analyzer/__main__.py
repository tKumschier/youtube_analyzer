# pylint: disable=wrong-import-position
import os
import sys

sys.path.append(os.path.dirname(__file__))

from apscheduler.schedulers.blocking import BlockingScheduler

from youtube_analyzer.main import main

if __name__ == "__main__":
    if "--test" in sys.argv:
        main()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, "cron", hour="8-21", minute="15", max_instances=1)
        print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
