import requests
from groq import Groq
import streamlit as st
import config

# إعداد عميل الذكاء الاصطناعي
client = None
try:
    client = Groq(api_key=config.GROQ_API_KEY)
except:
    pass

@st.cache_data
def fetch_content(content_type="movie", category="popular", region=None):
    """دالة موحدة لجلب الأفلام أو المسلسلات"""
    api_key = config.TMDB_API_KEY
    base_url = config.BASE_URL
    
    # تحديد نوع الميديا للرابط
    endpoint_type = "movie" if content_type == "movie" else "tv"
    
    # خريطة المناطق
    region_map = {
        "korea": "&with_original_language=ko",
        "india": "&with_original_language=hi", # بوليوود
        "arabic": "&with_original_language=ar",
        "turkey": "&with_original_language=tr",
        "spain": "&with_original_language=es",
        "japan": "&with_original_language=ja&with_genres=16", # أنيمي
    }

    url = ""
    # إذا تم اختيار دولة معينة نستخدم Discover
    if region and region in region_map:
        url = f"{base_url}/discover/{endpoint_type}?api_key={api_key}&language=ar-SA&sort_by=popularity.desc{region_map[region]}"
    else:
        # إذا كانت فئات عامة (رائج، قريبا، الخ)
        url = f"{base_url}/{endpoint_type}/{category}?api_key={api_key}&language=ar-SA"

    try:
        return requests.get(url).json().get('results', [])
    except:
        return []

def get_trailer(id, content_type="movie"):
    try:
        url = f"{config.BASE_URL}/{content_type}/{id}/videos?api_key={config.TMDB_API_KEY}"
        data = requests.get(url).json()
        for v in data.get('results', []):
            if v['type'] == "Trailer" and v['site'] == "YouTube":
                return f"https://www.youtube.com/watch?v={v['key']}"
    except:
        pass
    return None

def generate_analysis(title, overview, content_type="movie"):
    if not client: return "يرجى التحقق من مفتاح Groq API"
    
    type_ar = "فيلم" if content_type == "movie" else "مسلسل"
    prompt = f"""
    أنت ناقد سينمائي عالمي ساخر وذكي. اكتب مراجعة قصيرة وجذابة جداً باللغة العربية لـ {type_ar}: "{title}".
    القصة: {overview}
    
    التنسيق المطلوب:
    🎥 **القصة بعمق:** (شرح فلسفي سريع)
    🎭 **الأداء:** (من أبدع ومن أخفق)
    🍿 **هل يستحق؟:** (نعم/لا ولماذا، بلهجة عامية محترمة)
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=800
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "المحلل الذكي يأخذ استراحة قهوة الآن..."

def search_tmdb(query, content_type="movie"):
    url = f"{config.BASE_URL}/search/{content_type}?api_key={config.TMDB_API_KEY}&query={query}&language=ar-SA"
    return requests.get(url).json().get('results', [])

def semantic_search_ai(user_desc):
    """البحث بالوصف باستخدام الذكاء الاصطناعي"""
    if not client: return []
    try:
        # 1. نحول الوصف إلى عناوين إنجليزية
        prompt = f"Suggest 3 movie/TV show titles that match this description: '{user_desc}'. Return ONLY the English titles separated by commas, nothing else."
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
        titles = res.choices[0].message.content.split(',')
        
        results = []
        # 2. نبحث عن هذه العناوين في TMDB
        for t in titles:
            t = t.strip()
            # بحث سريع في الأفلام
            search = search_tmdb(t, "movie")
            if search: results.extend(search[:1])
    
        return results
    except:
        return []
