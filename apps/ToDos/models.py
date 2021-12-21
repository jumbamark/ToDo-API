from django.db import models
from helpers.models import TrackingModel
from authentication.models import User

# Create your models here.
class ToDo(TrackingModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title