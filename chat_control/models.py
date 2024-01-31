from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class StoredEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.receiver}"

    class Meta:
        ordering = ("timestamp",)
        verbose_name_plural = "Message"
