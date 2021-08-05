from django.contrib.auth import authenticate
from rest_framework import serializers

from .auth_by_telegram import Auth_by_telegram
from .models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    contacts = serializers.CharField(max_length=15)

    class Meta:
        model = Profile
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'full_name', 'password', 'token', 'contacts']

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return Profile.objects.create_user(**validated_data)




class LoginSerializer(serializers.Serializer):

    #user_id из Telegram
    contacts = serializers.CharField(max_length=15)

    class Meta:
        model = Profile
        fields = ['email', 'full_name', 'password', 'token', 'contacts']

    def validate(self, data):

        contacts = data.get('contacts', None)

        # Метод authenticate представляет собой кастомную аутентификацию по user_id из Telegram.
        # Об этом говорит строка
        # AUTHENTICATION_BACKENDS = ('filling_profile.auth_by_telegram.Auth_by_telegram',) в settings.py
        # Реализация метода прописана в auth_by_telegram.py
        user = authenticate(self, contacts=contacts)


        # Если пользователь с данными user_id не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                'A user with this Telegram user_id was not found.'
            )

        # Метод validate должен возвращать словарь проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'email': user.email,
            'username': user.full_name,
            'contacts': user.contacts,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    password = serializers.CharField(

        write_only=True
    )

    class Meta:
        model = Profile
        fields = ('email', 'full_name', 'password', 'token',)

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """
        print(f'serializers update validated_data:-----{validated_data}--------')
        # В отличие от других полей, пароли не следует обрабатывать с помощью
        # setattr. Django предоставляет функцию, которая обрабатывает пароли
        # хешированием и 'солением'. Это означает, что нам нужно удалить поле
        # пароля из словаря 'validated_data' перед его использованием далее.
        password = validated_data.pop('password', None)
        print(f'serializers update password:-----{password}--------')
        print(f'serializers update validated_data:-----{validated_data}--------')

        print(f'serializers update instance:-----{instance}--------')

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)
        print(f'serializers update instance:-----{instance}--------')
        if password is not None:
            # 'set_password()' решает все вопросы, связанные с безопасностью
            # при обновлении пароля, потому нам не нужно беспокоиться об этом.
            instance.set_password(password)

        # После того, как все было обновлено, мы должны сохранить наш экземпляр
        # User. Стоит отметить, что set_password() не сохраняет модель.
        instance.save()

        print(f'serialaizer:-----{instance.password}--------')
        return instance

