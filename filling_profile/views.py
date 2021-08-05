
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView



from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import Filling_Profile_form
from .models import Profile, Skills, Categories
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)


def index(request):
    if request.method == 'GET':
        full_name = request.GET.get('full_name')
        editing_profile = Profile.objects.filter(full_name=full_name).exists()

        if editing_profile:
            data = {"full_name": Profile.objects.get(full_name=full_name).full_name,
                    "email": Profile.objects.get(full_name=full_name).email,
                    "goal": Profile.objects.get(full_name=full_name).goal,
                    "language": Profile.objects.get(full_name=full_name).language,
                    "contacts": Profile.objects.get(full_name=full_name).contacts}

            form = Filling_Profile_form(data)
            skills_editing_profile = Profile.objects.get(full_name=full_name).skills
            if skills_editing_profile != None:
                skills_editing_profile_list = skills_editing_profile.split(',')
            else:
                skills_editing_profile_list = ''
            form.full_name = Profile.objects.get(full_name=full_name).full_name
            a = Profile.objects.get(full_name=full_name)
            form.email = a.email
            print(f'-----------------{form.full_name}------{form.email}--------------------------')


        else:
            form = Filling_Profile_form(request.GET)
            skills_editing_profile = None
            skills_editing_profile_list = None
            form.full_name = request.GET.get('full_name')
            form.email = request.GET.get('email')
            form.contacts = request.GET.get('contacts')

        skills = Skills.objects.all()
        categoriess = Categories.objects.all()


    return render(request, 'filling_profile/profile_form.html',
                  {'form': form, 'skills': skills, 'categoriess': categoriess,
                   'skills_editing_profile': skills_editing_profile,
                   'skills_editing_profile_list': skills_editing_profile_list})


def press_ok(request):
    if request.method == "POST":
        form = Filling_Profile_form(request.POST)
        prof = form.save(commit=False)
        prof.skills = request.POST.get('skills_list')
        editing_profile = Profile.objects.filter(full_name=prof.full_name).exists()
        if editing_profile:
            editing_profile = Profile.objects.get(full_name=prof.full_name)
            editing_profile.full_name = prof.full_name
            editing_profile.email = prof.email
            editing_profile.skills = prof.skills
            editing_profile.goal = prof.goal
            editing_profile.language = prof.language
            editing_profile.contacts = prof.contacts
            editing_profile.save()

        else:

            prof.save(force_insert=True)

    else:
        form = Filling_Profile_form

    return render(request, 'filling_profile/profile_form.html', {'form': form})


def login(request):
    return render(request, 'login.html')



class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        profile = request.data.get('profile', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('profile', {})

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    # работает по запросу GET
    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        user = request.data.get('profile', {})
        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # работает по запросу PUTCH
    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('profile', {})
        print(f'view update serializer_data:-----{serializer_data}--------')
        print(f'view update request.user:-----{request.user}--------')
        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        # serializer= self.serializer_class.update(self, request.user, )
        print(f'view update serializer:-----{serializer}--------')
        serializer.is_valid(raise_exception=True)
        print(f'view update serializer.is_valid:-----{serializer.is_valid(raise_exception=True)}--------')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)