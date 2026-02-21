from django.db import models

class MockedResource(models.Model):
    name = models.CharField(max_length=100)
    data = models.TextField()

    def __str__(self):
        return self.name
