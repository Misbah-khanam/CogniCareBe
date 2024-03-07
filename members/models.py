from django.db import models
from user.models import User


class Members(models.Model):
    
    name = models.CharField(max_length=100, default='')
    age = models.IntegerField()
    gender = models.CharField(max_length=100, default='')
    organisation = models.CharField(max_length=100, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return  self.name