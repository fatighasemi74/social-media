from django.db import models


from account.models import UserAccount, Data
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_time = models.DateTimeField("created time", auto_now_add=True)
    modified_time = models.DateTimeField("modified time", auto_now=True)

    class Meta:
        abstract = True




class Post(BaseModel):
     caption = models.TextField(blank=True, null=True, max_length=1000)
     user = models.ForeignKey(UserAccount, related_name='posts', on_delete=models.CASCADE)
     title = models.CharField(max_length=80, default='', blank=True, null=True)
     media_id = models.ManyToManyField(Data, related_name='postmedias', blank=True)


     class Meta:
         verbose_name = 'post'
         verbose_name_plural = 'posts'

     def __str__(self):
        return "{} ({})".format(self.user.username, self.id)



class Comment(BaseModel):
    caption = models.TextField()
    user = models.ForeignKey(UserAccount, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return self.caption

class Like(BaseModel):
    user = models.ForeignKey(UserAccount, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return "{} >> {}".format(self.user.username, self.post)