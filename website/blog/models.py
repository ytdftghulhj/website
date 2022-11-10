from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name_category = models.CharField(max_length=255)
    def __str__(self):
        return self.name_category


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank= True)
    created_at = models.DateTimeField(auto_now_add= True)
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
    email = models.CharField(max_length=255, unique= True)
    is_confirmed = models.BooleanField()
    role = models.CharField(
        max_length= 2,
        choices = Role.choices,
        default=Role.User,
    )
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.nickname

class Comments(models.Model):
    text_comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add= True)
    article = models.ForeignKey('Article', on_delete=models.PROTECT, null=True)
    author = models.ForeignKey('Users', on_delete=models.PROTECT, null=True)


