# api.py
import requests
from groq import Groq
import streamlit as st
import config

# إعداد العميل (AI Client)
client = None
try:
    client = Groq(api_key=config.GROQ_API_KEY)
except:
    pass

# --- 1. دوال الأفلام (MOVIES) ---
@st.cache_data
def fetch_movies(category="popular", region=None):
    base = config.BASE_URL
    key = config.TMDB_API_KEY
    
    # خريطة الدول (أكواد اللغات ومعايير الترتيب)
    region_map = {
        "korea": "&with_original_language=ko",
        "bollywood": "&with_original_language=hi",
        "arabic": "&with_original_language=ar",
        "china": "&with_original_language=zh",
        "japan": "&with_original_language=ja&with_genres=16", # أنيمي
        "turkey": "&with_original_language=tr",
        "spain": "&with_original_language=es",
    }

    # التحقق: هل هناك دولة محددة؟
    if region and region in region_map:
        url = f"{base}/discover/movie?api_key={key}&language=ar-SA&sort_by=popularity.desc{region_map[region]}"
    else:
        url = f"{base}/movie/{category}?api_key={key}&language=ar-SA"
    
    return requests.get(url).json().get('results', [])

# --- 2. دوال المسلسلات (TV SHOWS) - هذا هو الجزء الجديد المفقود عندك ---
@st.cache_data
def fetch_tv_shows(category="popular", region=None):
    base = config.BASE_URL
    key = config.TMDB_API_KEY
    
    # خريطة الدول للمسلسلات
    region_map = {
        "korea": "&with_original_language=ko", # K-Drama
        "arabic": "&with_original_language=ar",
        "turkey": "&with_original_language=tr", # مسلسلات تركية
        "japan": "&with_original_language=ja&with_genres=16", # أنيمي
        "spain": "&with_original_language=es",
    }

    if region and region in region_map:
        url = f"{base}/discover/tv?api_key={key}&language=ar-SA&sort_by=popularity.desc{region_map[region]}"
    else:
        # فئات المسلسلات: popular, top_rated, on_the_air
        url = f"{base}/tv/{category}?api_key={key}&language=ar-SA"
    
    return requests.get(url).json().get('results', [])

# --- 3. البحث الشامل (أفلام ومسلسلات) ---
def search_tmdb(query, type="movie"):
    # type إما 'movie' أو 'tv'
    url = f"{config.BASE_URL}/search/{type}?api_key={config.TMDB_API_KEY}&query={query}&language=ar-SA"
    return requests.get(url).json().get('results', [])

# --- 4. جلب التريلر ---
def get_trailer(id, type="movie"):
    try:
        url = f"{config.BASE_URL}/{type}/{id}/videos?api_key={config.TMDB_API_KEY}"
        data = requests.get(url).json()
        for v in data['results']:
            if v['type'] == "Trailer" and v['site'] == "YouTube":
                return f"https://www.youtube.com/watch?v={v['key']}"
    except: pass
    return None

# --- 5. البحث الذكي (AI) ---
def semantic_search(user_description):
    if not client: return []
    try:
        # نطلب من الذكاء الاصطناعي أن يبحث عن أفلام أو مسلسلات
        prompt = f"Find 3 movies or TV series matching: '{user_description}'. Return ONLY English titles separated by commas."
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        titles = [t.strip() for t in completion.choices[0].message.content.split(',')]
        results = []
        for t in titles:
            # نبحث في الأفلام أولاً
            res = requests.get(f"{config.BASE_URL}/search/movie?api_key={config.TMDB_API_KEY}&query={t}").json().get('results', [])
            if not res:
                # إذا لم نجد، نبحث في المسلسلات
                res = requests.get(f"{config.BASE_URL}/search/tv?api_key={config.TMDB_API_KEY}&query={t}").json().get('results', [])
            
            if res: 
                # نضيف علامة لنعرف هل هو فيلم أم مسلسل
                item = res[0]
                item['media_type'] = 'movie' if 'title' in item else 'tv'
                results.append(item)
        return results
    except: return []

# --- 6. المحلل العبقري ---
def generate_analysis(title, overview, type="movie"):
    if not client: return "⚠️ يرجى التحقق من مفتاح الذكاء الاصطناعي."
    
    type_ar = "فيلم" if type == "movie" else "مسلسل"
    
    prompt = f"""
    أنت ناقد فني عبقري. اكتب تقريراً حصرياً وشيقاً جداً باللغة العربية عن {type_ar}: "{title}".
    
    غطِّ النقاط التالية بأسلوب إبداعي:
    1. 🧐 **العمق الفني:** الرسالة والقصة.
    2. 🎬 **حقائق:** كواليس أو حقائق عن الممثلين والمواسم.
    3. 🗣️ **رأي الجمهور:** ماذا يقول الناس في السوشيال ميديا بصدق؟
    4. 🧠 **الخلاصة:** هل يستحق المشاهدة؟

    نبذة: {overview}
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"عذراً، المحلل مشغول. الخطأ: {e}"