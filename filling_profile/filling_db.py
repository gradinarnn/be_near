from web.apps.filling_profile.models import Skills, Categories

category = (
    "📟 Tech", "☘️ Wellness", "🔥 Trends", "🦉 Knowledge", "💬 Languages", "💭 Art", "🏆 Sports",
    "🤹🏼‍♀️ Entertaiment")

category_tech = (
    "🧭 Marketing", "☁️ SaaS", "🤖 Engineering", "💸 Investing", "🐇 Crypto", "🦄 Startups", "🧠 AI", "🚀 Product",
    "👓 AR/VR", "🛍 DTC")
category_wellness = (
    "🧘🏻‍♂️ Meditation", "🏕 Outdoors", "🍎 Health", "🥕 Veganism", "🌽 Nutrition", "🚑 Medicine",
    "🏃🏻‍♀️ Fitness",
    "🏋🏻‍♂️ Weights", "🌱 Mindfulness")

category_trends = ("🏦 Stocks", "🦁 Entrepreneurship", "🏠 Real Estate", "🎯 Pitch Practice", "⚡️ Small Business")

category_knowlenge = (
    "🪴 Education", "🧬 Biology", "🐳 Philosophy", "🪞 Psychology", "🔮 The Future", "🪖 History", "⚗️ Science",
    "🧮 Math", "🧲 Physics", "🛸 Space")

category_languages = (
    "🇬🇧 British English", "🇺🇸 American English", "🇷🇺 Russian", "🇫🇷 French", "🇩🇪 German", "🇺🇦 Ukranian",
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