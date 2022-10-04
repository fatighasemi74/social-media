from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_time = models.DateTimeField("created time", auto_now_add=True)
    modified_time = models.DateTimeField("modified time", auto_now=True)

    class Meta:
        abstract = True

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



class Relation(BaseModel):
    from_user = models.ForeignKey(UserAccount, related_name='followingss', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserAccount, related_name='follewrss', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'

    def __str__(self):
        return "{} >> {}".format(self.from_user.username, self.to_user.username)


