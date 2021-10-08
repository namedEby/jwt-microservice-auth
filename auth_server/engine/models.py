""" Django database models """

# Native imports
import random
import string

# Module imports
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth.base_user import BaseUserManager

user_modes = (
    (1, 'investor'),
    (2, 'administrator')
)


class UserManager(BaseUserManager):
    """ Manager for the User model """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the email and password."""

        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """ Method to create a user """
        extra_fields.setdefault(
            'is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """ Method to create a super user """

        extra_fields.setdefault(
            'is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ User Abstract model """

    email = models.EmailField(unique=True)
    mode = models.IntegerField(choices=user_modes, default=1, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    secret = models.TextField(default="")
    secret2 = models.TextField(default="")
    secret_size = models.IntegerField(default=156)

    def __secret_generator(self):
        """ Returns generated secret """
        return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(self.secret_size))

    def generate_new_secret(self):
        """ Generates new access secret """
        self.secret = self.__secret_generator()
    
    def generate_new_secret2(self):
        """ Generates new refresh secret """
        self.secret2 = self.__secret_generator()

    def retrieve_secret(self):
        """ returns access secret """
        return self.secret

    def retrieve_secret2(self):
        """ returns refresh secret """
        return self.secret2

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
