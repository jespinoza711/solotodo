from celery.task import Task
from celery.registry import tasks
from datetime import datetime

class UpdateStore(Task):
    def run(self, registry):
        registry.status = 'En proceso'
        registry.save()
        try:
            registry.store.update_products_from_webpage(update_shpes_on_finish = True)
            registry.end_datetime = datetime.now()
            registry.status = 'Completado'
        except:
            registry.status = 'Error'
        
        registry.save()

tasks.register(UpdateStore)
