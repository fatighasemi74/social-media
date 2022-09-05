from django.db import models
from blogapi import settings


from django.contrib.auth.models import User

class UserAccount(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_account')
    name = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='account/media', null=True, blank=True,  height_field=None, width_field=None, max_length=100)
    bio = models.TextField(blank=True, null= True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    allowed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'userAccount'
        verbose_name_plural = 'userAccounts'

    def __str__(self):
        return self.name

    # @property
    # def default_picture(self):
    #     if self.profile_picture:
    #         return "{}{}".format(settings.MEDIA_URL, self.profile_picture)
    #     return 'account/media/pic.jpeg'



