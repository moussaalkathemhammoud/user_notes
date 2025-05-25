from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password,first_name,last_name):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True,primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def id(self):
        return self.email


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    user =models.ForeignKey(MyUser,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    color =  models.CharField(max_length=10, default='#000000')