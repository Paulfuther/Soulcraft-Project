from django.db import models


class ErrorLog(models.Model):
    path = models.CharField(max_length=1024)
    status_code = models.IntegerField()
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.status_code} - {self.path}"
