from django.db import models
from talvido_app.models import Talvidouser, BaseModel
from chat.helpers import encrypt_message


class Chat(BaseModel):
    sender = models.ForeignKey(
        Talvidouser,
        verbose_name="Sender",
        on_delete=models.CASCADE,
        related_name="sender_chat",
    )
    reciever = models.ForeignKey(
        Talvidouser,
        verbose_name="Reciever",
        on_delete=models.CASCADE,
        related_name="reciever_chat",
    )
    message = models.TextField(verbose_name="message", max_length=500)
    seen = models.BooleanField(verbose_name="Seen", default=False)
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.message = encrypt_message(message=self.message)
        super().save(*args, **kwargs)
