from django.contrib.auth import authenticate
from rest_framework import serializers

import be_near.constants
from .models import Profile, Profile_for_Metting


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    # password = serializers.CharField(
    #     write_only=True
    # )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    contacts = serializers.CharField(max_length=15)

    class Meta:
        model = Profile
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'full_name', 'token', 'contacts']

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return Profile.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    # user_id из Telegram
    contacts = serializers.CharField(max_length=15)
    machine_token = serializers.CharField(max_length=20, write_only=True)
    meeting_status = serializers.CharField(max_length=20, read_only=True)
    token = serializers.CharField(max_length=20, read_only=True)
    full_name = serializers.CharField(max_length=50, read_only=True)
    email = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'full_name', 'password', 'token', 'contacts']

    def validate(self, data):
        contacts = data.get('contacts', None)
        machine_token = data.get('machine_token', None)

        if machine_token == be_near.constants.a:

            # Метод authenticate представляет собой кастомную аутентификацию по user_id из Telegram.
            # Об этом говорит строка
            # AUTHENTICATION_BACKENDS = ('filling_profile.auth_by_telegram.Auth_by_telegram',) в settings.py
            # Реализация метода прописана в auth_by_telegram.py
            user = authenticate(self, contacts=contacts)

            print(f'-----------LoginSerializer: user = {user}')
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
                'token': user.token,
                'meeting_status': user.meeting_status

            }
        else:
            return {
                'contacts': 'Not found'

            }


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    # password = serializers.CharField(
    #
    #     write_only=True
    # )

    class Meta:
        model = Profile
        fields = ('email', 'full_name', 'token', 'contacts', 'meeting_status')

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        # password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        
        try:
            profile= Profile_for_Metting.objects.get(profile=Profile.objects.get(contacts=instance.contacts))
            profile_exist=True
            print(f'Профиль найден')
        except Profile_for_Metting.DoesNotExist:
            profile_exist=False
            print(f'Профиль не найден')


        if (instance.meeting_status == 'waitting') and (profile_exist==False):
            profile_for_meeting = Profile_for_Metting(profile=Profile.objects.get(contacts=instance.contacts))
            profile_for_meeting.save()

        elif ((instance.meeting_status == 'not ready') or (instance.meeting_status == 'meetting')) and (profile_exist==True):
            Profile_for_Metting.objects.filter(profile=Profile.objects.get(contacts=instance.contacts)).delete()

        instance.save()

        return instance
