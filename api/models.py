from django.db import models
from django.contrib.auth.models import User

# Create your models here.

USER_PROFILE_DEST = 'users/avatars/'


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField()
    avatar = models.ImageField(upload_to=USER_PROFILE_DEST)
    birthdate = models.DateField(null=True)
    i_like = models.TextField(null=True)
    i_dislike = models.TextField(null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'


class Tag(models.Model):

    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Post(models.Model):

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Friendship(models.Model):

    id_user1 = models.IntegerField()
    id_user2 = models.IntegerField()
    relationship = models.CharField(max_length=10, choices=(
        ('FRIENDS', 'User1 is friend of User2'),
        ('FOLLOWER', 'User1 is follower of User2'),
        ('FOLLOWING', 'User1 is following by User2')
    ))

    class Meta:
        verbose_name = 'отношение между пользователями'
        verbose_name_plural = 'отношения между пользователями'