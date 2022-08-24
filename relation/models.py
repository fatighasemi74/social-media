from django.db import models

from django.contrib.auth.models import User





class BaseModel(models.Model):
    created_time = models.DateTimeField("created time", auto_now_add=True)
    modified_time = models.DateTimeField("modified time", auto_now=True)

    class Meta:
        abstract = True


class Relation(BaseModel):
    from_user = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follewrs', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'

    def __str__(self):
        return "{} >> {}".format(self.from_user.username, self.to_user.username)