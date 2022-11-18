from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name_category = models.CharField(max_length=255)

    def __str__(self):
        return self.name_category


class Tags(models.Model):
    name_tag = models.TextField(max_length=255, )

    def __str__(self):
        return self.name_tag


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank= True)
    author = models.ForeignKey('Users', on_delete=models.PROTECT, null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title


class Role(models.TextChoices):
    Admin = 'AD',_('Admin')
    User = 'US', _('User')


class Users(models.Model):
    nickname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    is_confirmed = models.BooleanField()
    role = models.CharField(
        max_length= 2,
        choices = Role.choices,
        default=Role.User,
    )
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    subscriptions = models.ManyToManyField('Users', through='Subscriptions')

    def __str__(self):
        return self.nickname


class Subscriptions(models.Model):
    from_who = models.ForeignKey('Users', on_delete=models.PROTECT, null=True, related_name='from_who')
    to_who = models.ForeignKey('Users', on_delete=models.PROTECT, null=True, related_name='to_who')
    is_notification = models.BooleanField()


class Comments(models.Model):
    text_comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add= True)
    article = models.ForeignKey('Article', on_delete=models.PROTECT, null=True)
    author = models.ForeignKey('Users', on_delete=models.PROTECT, null=True, related_name='author')
    likes = models.ManyToManyField('Users',  blank=True, related_name='likes')
    parent_comment = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, related_name='replies', null=True)


class Notification(models.Model):
    subscriber = models.ForeignKey('Users', on_delete=models.PROTECT, null=True)
    content = models.ForeignKey('Article', on_delete=models.PROTECT, null=True)

