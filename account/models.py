from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class BaseModel(models.Model):
    created_time = models.DateTimeField("created time", auto_now_add=True)
    modified_time = models.DateTimeField("modified time", auto_now=True)

    class Meta:
        abstract = True

#
# class Medias(BaseModel):

#     #
    TYPE_CHOICES = (
        (0, "ProfilePicture"),
        (1, "PostImage"),
    )
#     media_type = models.CharField(max_length=30)
#     media_file = models.FileField(upload_to='content/media', default=1, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))])
#     content_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Media"
#         verbose_name_plural = "Medias"

    # def __str__(self):
    #     return '{}'.format(str(self.user))

class Data(BaseModel):
    TYPE_CHOICES = (
        (0, "ProfilePicture"),
        (1, "PostImage"),
    )
    media_type = models.IntegerField(choices=TYPE_CHOICES)
    media_file = models.FileField(upload_to='data/content/media', validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))])
    content_id = models.IntegerField()

    class Meta:
        verbose_name = "Data"
        verbose_name_plural = "Datas"

    def __str__(self):
        return '{} >> {}'.format(self.media_type, self.content_id)

class UserAccount(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_account')
    name = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='account/media', null=True, blank=True,  height_field=None, width_field=None, max_length=100)
    bio = models.TextField(blank=True, null= True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    allowed = models.BooleanField(default=False)
    media_id = models.ForeignKey(Data, related_name='userdatas', null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'userAccount'
        verbose_name_plural = 'userAccounts'

    def __str__(self):
        return self.name



class Relation(BaseModel):
    from_user = models.ForeignKey(UserAccount, related_name='followings', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserAccount, related_name='follewrs', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'

    def __str__(self):
        return "{} >> {}".format(self.from_user.username, self.to_user.username)


