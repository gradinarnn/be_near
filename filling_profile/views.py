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







        category = (
            "📟 Tech", "☘️ Wellness", "🔥 Trends", "🦉 Knowledge", "💬 Languages", "💭 Art", "🏆 Sports",
            "🤹🏼‍♀️ Entertaiment")

        category_tech = (
            "🧭 Marketing", "☁️ SaaS", "🤖 Engineering", "💸 Investing", "🐇 Crypto", "🦄 Startups", "🧠 AI",
            "🚀 Product",
            "👓 AR/VR", "🛍 DTC")
        category_wellness = (
            "🧘🏻‍♂️ Meditation", "🏕 Outdoors", "🍎 Health", "🥕 Veganism", "🌽 Nutrition", "🚑 Medicine",
            "🏃🏻‍♀️ Fitness",
            "🏋🏻‍♂️ Weights", "🌱 Mindfulness")

        category_trends = (
        "🏦 Stocks", "🦁 Entrepreneurship", "🏠 Real Estate", "🎯 Pitch Practice", "⚡️ Small Business")

        category_knowlenge = (
            "🪴 Education", "🧬 Biology", "🐳 Philosophy", "🪞 Psychology", "🔮 The Future", "🪖 History", "⚗️ Science",
            "🧮 Math", "🧲 Physics", "🛸 Space")

        category_languages = (
            "🇬🇧 British English", "🇺🇸 American English", "🇷🇺 Russian", "🇫🇷 French", "🇩🇪 German",
            "🇺🇦 Ukranian",
            "🇨🇳 Mandarin", "🇮🇩 Indonesian", "🇪🇬 Arabic", "🇧🇷 Portuguese", "🇪🇸 Spanish", "🇯🇵 Japanese")

        category_art = (
            "🐼 Design", "📝  Writing", "📏 Architecture", "📚 Books", "🍧 Food&Drink", "📸 Photography", "💄 Beauty",
            "👘 Fashion", "👽 Sci-Fi", "🎭 Theater", "💃🏽 Dance", "🌋 Art")

        category_sports = (
            "🚴🏼‍♂️ Cycling", "🏏 Cricket", "🏌🏽‍♀️ Golf", "⚽️ Soccer", "🤼 MMA", "⚾️ Baseball", "🏎 Formula 1",
            "⛹🏽‍♀️ Basketball", "🏈 Football", "🎾 Tennis", "⛸ Ice skating", "🛹 Skateboard", "🚣🏾‍♂️ Rowing",
            "🏊🏻‍♀️ Swimming",
            "🏒 Hockey")

        category_intertaiment = (
            "🎮 Gaming", "🎟 Performances", "🎙 Storytelling", "😆 Comedy", "🎧 Music", "🦸🏻‍♀️ Celebrities",
            "😻 Anime & Manga",
            "🚙 Variety", "📹 Movies", "🤩 Fun", "👩🏽‍🎓 Trivia", "📻 Podcasts", "🎤 Karaoke", "☕️ Advice",
            "📺 Television")

        all = (category_tech, category_wellness, category_trends, category_knowlenge, category_languages, category_art,
               category_sports, category_intertaiment)

        category_db = Categories()
        skill_db = Skills()
        a = 0
        b = 0
        for i in category:

            # skills_categories_db.add_categories(a+1, i)
            category_db.category_title = i
            category_db.skill_id = a + 1

            print(f'----------------------------{i}-------------------------')
            category_db.save(force_insert=True)

            for j in all[a]:
                b += 1
                skill_db.skill_title = j
                skill_db.skill_category = i
                skill_db.skill_id = b
                skill_db.save(force_insert=True)
                # skills_categories_db.add_skills(a+1,b,j)

            a += 1








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
