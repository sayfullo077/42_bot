from django.db import models

class BotUser(models.Model):
    user_id = models.CharField(max_length=15, verbose_name="User ID")
    name = models.CharField(max_length=155, verbose_name="Telegram Name", null=True, blank=True)
    username = models.CharField(max_length=35, verbose_name="Username", null=True, blank=True)
    contact = models.CharField(max_length=15, verbose_name="Contact")
    code = models.CharField(max_length=7, verbose_name="Code", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    class Meta:
        verbose_name = "Bot User"
        verbose_name_plural = "Bot Users"

    def __str__(self):
        return str(self.name)
