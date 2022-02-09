from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, name=None, password=None, phone_num=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
            phone_num = phone_num
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, name=None, password=None, phone_num=None):
        user = self.create_user(
            email,
            date_of_birth=date_of_birth,
            name=name,
            phone_num=phone_num
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)
    date_of_birth = models.DateField(verbose_name="생년월일", null=False)
    #전화번호 유효성검사
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_num = models.CharField(verbose_name="전화번호",validators=[phoneNumberRegex], max_length=16, unique=True)
    age = models.PositiveIntegerField(default=0, null=False, blank=False)
    name = models.CharField(verbose_name="이름", max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name', 'phone_num']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin