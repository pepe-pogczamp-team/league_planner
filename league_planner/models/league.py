from django.db.models import Model
from django.db import models


class League(Model):
    name = models.CharField(max_length=50)
