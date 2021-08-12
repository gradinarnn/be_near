import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models
from django.db.models import CASCADE


class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, full_name, email, password=None, contacts=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if full_name is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(full_name=full_name, email=self.normalize_email(email), contacts=contacts)
        # user.set_password(password)
        user.save()

        return user

    def create_superuser(self, full_name, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(full_name, email, password)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user






class Profile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField('полнейшее имя', max_length=50, blank=True)
    email = models.CharField('email адрес', max_length=50, null=True, blank=True, unique=True)
    skills = models.CharField('навыки', max_length=150, null=True)
    goal = models.IntegerField('цель общенщения', default=None, null=True, blank=True)
    contacts = models.CharField('Telegram', max_length=15, default=[''], null=True, blank=True)
    language = models.CharField('язык', max_length=20, default='', null=True, blank=True)
    meeting_status = models.CharField(max_length=20, default="not ready", null=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Profile'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']


    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()


    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.full_name

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.full_name

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            "id": self.pk,
            # "exp": int(dt.strftime('%S'))
        }, 'q', algorithm='HS256')

        return token


class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_title = models.CharField(max_length=50)
    skill_category = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.skill_category}: {self.skill_title}'

    class Meta:
        db_table = 'Skills'


class Categories(models.Model):
    skill_id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category_title}'

    class Meta:
        db_table = 'Categories'


class Profile_for_Metting(models.Model):
    profile = models.ForeignKey(Profile, on_delete=CASCADE, blank=True)

    class Meta:
        db_table = 'Profile_for_Metting'


class Meet(models.Model):
    id = models.AutoField(primary_key=True)
    first_profile = models.ForeignKey(Profile, on_delete=CASCADE, related_name='first_profile_id', blank=True)
    second_profile = models.ForeignKey(Profile, on_delete=CASCADE, related_name='second_profile_id', blank=True)
    meet_id = models.CharField(max_length=10, null=True)
    date_meeting = models.DateField(default=datetime.now(), null=True)
    feedback = models.CharField(max_length=10, null=True)
    goal_id = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Meet'
