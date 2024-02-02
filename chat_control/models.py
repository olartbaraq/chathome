from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class StoredEmail(models.Model):
    user = models.IntegerField(default=1)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        get_user_model(), related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.receiver}"

    class Meta:
        ordering = ("timestamp",)
        verbose_name_plural = "Message"
