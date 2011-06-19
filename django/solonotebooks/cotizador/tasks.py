import pycurl
from celery.task import Task
from celery.registry import tasks

class CheckWebsiteTask(Task):

    def run(self, ip, **kwargs):

        try:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, ip)
            c.setopt(pycurl.TIMEOUT, 10)

            c.perform()

        except Exception, e:
            print e

tasks.register(CheckWebsiteTask)
