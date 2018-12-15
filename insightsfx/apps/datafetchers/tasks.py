from celery import task
from .schedulers import CompareScheduler
from .models import CompareCache

@task(bind=True)
def RunAllFetchers(self):
    try:
        # Schdeule Government
        t = CompareCache.objects.create(
            extractor = "government"
        )
        CompareScheduler(t.id).start()
    except Exception as e:
        raise self.retry(exc=e, max_retried=3)