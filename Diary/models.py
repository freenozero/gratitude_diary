from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self, username, password, email, phone_num):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username=self.model.normalize_username(username),
            phone_num = phone_num,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, phone_num):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            phone_num=phone_num,
        )

        user.is_admin = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255,
                              unique=True,)
    username = models.CharField(max_length=30)
    phone_num = models.IntegerField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'email' #usernameFild를 email로
    REQUIRED_FIELDS = ['phone_num','username'] #필수로 받고 싶은 필드

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
