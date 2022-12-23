from django.db import models
from django.contrib.auth.models import  PermissionsMixin, AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from .managers import CustomUserManager


class MyUserManager(BaseUserManager):
    def _create_user(self, email, nickname, password, **extra_fields):
        if not email:
            raise ValueError("Вы не ввели Email")
        if not nickname:
            raise ValueError("Вы не ввели Логин")
        user = self.model(
            email=self.normalize_email(email),
            username=nickname,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class Category(models.Model):
    name_category = models.CharField(max_length=255)

    def __str__(self):
        return self.name_category


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank= True)
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Role(models.TextChoices):
    Admin = 'AD',_('Admin')
    User = 'US', _('User')


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.User,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    subscriptions = models.ManyToManyField('CustomUser', through='Subscriptions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = MyUserManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return self.email


class Subscriptions(models.Model):
    from_who = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True, related_name='from_who')
    to_who = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True, related_name='to_who')
    is_notification = models.BooleanField()


class Comments(models.Model):
    text_comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add= True)
    article = models.ForeignKey('Article', on_delete=models.PROTECT, null=True)
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True, related_name='author')
    likes = models.ManyToManyField('CustomUser',  blank=True, related_name='likes')
    parent_comment = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, related_name='replies', null=True)


class Notification(models.Model):
    subscriber = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True)
    content = models.ForeignKey('Article', on_delete=models.PROTECT, null=True)


