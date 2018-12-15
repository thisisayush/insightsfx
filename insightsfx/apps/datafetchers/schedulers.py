from .utils import GovernmentExtractor
from .models import CompareCache

class CompareScheduler:

    def __init__(self, task_obj):
        self.obj = task_obj

    def start(self):
        try:
            if self.obj is None or not self.can_process():
                return None
            
            if self.obj.completed:
                return True

            self.start_processing()

            self.set_status(CompareCache.COMPLETED)

            return True
        except Exception as e:
            self.set_status(CompareCache.FAILED, str(e))
            raise
    
    def start_processing(self):
        
        extractor = self.obj.extractor

        reader = None
        if extractor == "government":
            reader = GovernmentExtractor()
        else:
            raise self.UnsupportedExtractor(extractor)

        # Set the Status to Processing
        self.set_status(CompareCache.PROCESSING)
        
        # Start Processing
        reader.process()

    def can_process(self):
        if self.obj.status not in [CompareCache.COMPLETED, CompareCache.PROCESSING]:
            return True
        
        return False

    def set_status(self, status, msg=None):
        self.obj.status = status
        if self.obj.status == CompareCache.COMPLETED:
            self.obj.status_message = "Completed"
        elif self.obj.status == CompareCache.PROCESSING:
            self.obj.status_message = "Processing Started"
        if msg:
            self.obj.status_message = msg
        self.obj.save()

    class UnsupportedExtractor(Exception):
        pass