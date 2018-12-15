from django.db import models

app_label = "datafetchers"

class CompareCache(models.Model):
    
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

    status_choices = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    )

    extractor = models.CharField(max_length=255)
    status = models.CharField(choices = status_choices, max_length = 20, default=PENDING)
    status_message = models.TextField(null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    completed = models.BooleanField(default=False)
