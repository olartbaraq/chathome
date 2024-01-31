from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class StoredEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    class Meta:
        ordering = ("timestamp",)
        verbose_name_plural = "Message"
