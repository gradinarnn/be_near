import psycopg2
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import ListView

from .models import Profile, Skills, Categories
from .forms import Filling_Profile_form


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
