from django.contrib import admin

from .models import Profile, Skills, Categories, Profile_for_Metting, Meet

admin.site.register(Profile)
admin.site.register(Skills)
admin.site.register(Categories)
admin.site.register(Profile_for_Metting)
admin.site.register(Meet)

