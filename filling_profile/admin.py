from django.contrib import admin

from .models import Profile, Skill, Category, Profile_for_Metting, Meet

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Profile_for_Metting)
admin.site.register(Meet)

