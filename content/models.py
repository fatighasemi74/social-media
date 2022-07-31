from django.db import models
from django.core.validators import FileExtensionValidator


from account.models import UserAccount

class BaseModel(models.Model):
    created_time = models.DateTimeField("created time", auto_now_add=True)
    modified_time = models.DateTimeField("modified time", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):
     caption = models.TextField(blank=True, null=True, max_length=1000)
     user = models.ForeignKey(UserAccount, related_name='posts', on_delete=models.CASCADE)

     class Meta:
         verbose_name = 'post'
         verbose_name_plural = 'posts'

     def __str__(self):
        return "{} ({})".format(self.user.username, self.id)


class Media(BaseModel):
    IMAGE = 1
    VIDEO = 2

    TYPE_CHOICES = (
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    )
    media_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=IMAGE )
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='content/media', validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png'))])

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"

    def __str__(self):
        return '{}'.format(str(self.post))