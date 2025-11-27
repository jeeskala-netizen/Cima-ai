import requests
from groq import Groq
import streamlit as st
import config
import random
import base64 

# --- 1. إعداد العميل (Setup) ---
client = None
try:
    if hasattr(config, 'GROQ_API_KEY') and config.GROQ_API_KEY:
        client = Groq(api_key=config.GROQ_API_KEY)
    else:
        print("تحذير: مفتاح GROQ_API_KEY غير موجود في ملف الإعدادات.")
except Exception as e:
    print(f"خطأ في الاتصال بـ Groq: {e}")

# --- 2. دوال البحث والجلب (TMDB) ---

@st.cache_data
def fetch_content(content_type="movie", category="popular", region=None):
    """جلب الأفلام أو المسلسلات حسب الفئة والدولة"""
    api_key = config.TMDB_API_KEY
    base_url = config.BASE_URL
    endpoint_type = "movie" if content_type == "movie" else "tv"
    
    region_map = {
        "korea": "&with_original_language=ko",
        "india": "&with_original_language=hi", 
        "arabic": "&with_original_language=ar",
        "turkey": "&with_original_language=tr",
        "spain": "&with_original_language=es",
        "japan": "&with_original_language=ja&with_genres=16", 
    }

    url = ""
    if region and region in region_map:
        url = f"{base_url}/discover/{endpoint_type}?api_key={api_key}&language=ar-SA&sort_by=popularity.desc{region_map[region]}"
    else:
        url = f"{base_url}/{endpoint_type}/{category}?api_key={api_key}&language=ar-SA"

    try:
        return requests.get(url).json().get('results', [])
    except:
        return []

def search_tmdb(query, content_type="movie"):
    """البحث المباشر بالاسم في TMDB"""
    try:
        # استخدام search/multi لضمان العثور على العنوان سواء كان فيلماً أو مسلسلاً
        url = f"{config.BASE_URL}/search/multi?api_key={config.TMDB_API_KEY}&query={query}&language=ar-SA"
        return requests.get(url).json().get('results', [])
    except:
        return []

def get_trailer(id, content_type="movie"):
    """جلب رابط التريلر من يوتيوب"""
    try:
        url = f"{config.BASE_URL}/{content_type}/{id}/videos?api_key={config.TMDB_API_KEY}"
        data = requests.get(url).json()
        for v in data.get('results', []):
            if v['type'] == "Trailer" and v['site'] == "YouTube":
                return f"https://www.youtube.com/watch?v={v['key']}"
    except:
        pass
    return None

def get_watch_providers(id, content_type="movie"):
    """جلب منصات المشاهدة المتاحة في السعودية/المنطقة العربية"""
    try:
        url = f"{config.BASE_URL}/{content_type}/{id}/watch/providers?api_key={config.TMDB_API_KEY}"
        data = requests.get(url).json()
        # نركز على المنطقة العربية (SA = السعودية كمثال للسوق العربي)
        if 'results' in data and 'SA' in data['results']:
            return data['results']['SA'].get('flatrate', []) # flatrate تعني اشتراك مثل نتفليكس
    except:
        pass
    return []

# --- 3. دوال الذكاء الاصطناعي (AI Functions) ---

def generate_analysis(title, overview, content_type="movie"):
    """المحلل الفني (Genius Mode)"""
    if not client: return "عذراً، خدمة الذكاء الاصطناعي غير متصلة."
    
    type_ar = "فيلم" if content_type == "movie" else "مسلسل"
    prompt = f"""
    Analyze this {type_ar}: "{title}". Overview: {overview}.
    Write a short, engaging review in Arabic.
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"المحلل مشغول حالياً: {e}"

def semantic_search_ai(user_desc):
    """البحث الدلالي (بالوصف)"""
    if not client: return []
    try:
        prompt = f"Suggest 3 movie/TV titles matching: '{user_desc}'. Return ONLY English titles separated by commas."
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        titles = res.choices[0].message.content.split(',')
        results = []
        for t in titles:
            search = search_tmdb(t.strip())
            if search: results.extend(search[:1])
        return results
    except: return []

def chat_with_ai_formatted(messages, persona="الصديق الناصح 🤝"):
    """شات بوت متعدد الشخصيات ومصمم لإرجاع أسماء الأفلام"""
    if not client: return "عذراً، أنا في استراحة قهوة ☕ (تأكد من إعدادات الـ API)."
    
    # تعريف شخصيات المساعد
    personas = {
        "الصديق الناصح 🤝": """
            You are CimaBot, a helpful and friendly movie consultant. 
            Tone: Warm, welcoming, and balanced.
        """,
        "الناقد القاسي 🧐": """
            You are a snobbish, hard-to-please film critic. You hate cliché blockbusters.
            Tone: Sarcastic, intellectual, slightly arrogant. Use words like "سينماتوغرافي", "سردي", "مبتذل".
            Prefer artistic and hidden gems over popular Marvel movies.
        """,
        "الجوكر الساخر 🤡": """
            You are a comedian movie bot. You MUST make a joke about every movie you suggest.
            Tone: Funny, sarcastic, casual.
        """,
        "المتحمس (Fanboy) 🤩": """
            You are a super hyped movie geek! You love action, anime, and epic moments.
            Tone: High energy! Use lots of emojis like 🔥🚀🤯.
        """
    }
    
    selected_prompt = personas.get(persona, personas["الصديق الناصح 🤝"])

    core_instructions = """
    LANGUAGE RULES (STRICT):
    1. Speak ONLY in Arabic.
    2. Do NOT use Chinese, Korean, Japanese, or any other scripts. NEVER mix languages.
    3. The ONLY exception is the Movie/Show Title, which MUST be in English inside brackets.
    
    FORMATTING RULE:
    When you recommend a specific movie or show, put its Original English Title inside brackets like this: [Inception].
    After the title, explain WHY you chose it in Arabic based on your persona.
    
    Example output:
    "أنصحك بمشاهدة [The Dark Knight] لأنه يقدم صراعاً نفسياً عميقاً."
    
    Do NOT output lists. Speak naturally like a friend.
    """
    
    final_system_prompt = selected_prompt + "\n" + core_instructions
    
    # إدارة الرسائل لتضمين التعليمات
    if messages and messages[0].get("role") != "system":
        full_messages = [{"role": "system", "content": final_system_prompt}] + messages
    else:
        full_messages = messages
        if not full_messages:
             full_messages = [{"role": "system", "content": final_system_prompt}]
        else:
             full_messages[0] = {"role": "system", "content": final_system_prompt}
    
    try:
        completion = client.chat.completions.create(
            messages=full_messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7, 
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ تقني في الشات: {e}"

def analyze_dna(favorites_list):
    """تحليل نفسية المستخدم بناءً على أفلامه المفضلة"""
    if not client: return "عذراً، المحلل النفسي في إجازة 🏖️."
    fav_movies = ", ".join(favorites_list)
    prompt = f"""
    Act as a Psychology & Film Expert speaking Arabic.
    User's favorite movies are: {fav_movies}.
    Task 1: Analyze the user's "Cinematic DNA". What does this taste say about their personality? (Write 2-3 sentences in Arabic).
    Task 2: Recommend 3 NEW movies based on this DNA. Put English titles in [Brackets].
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ: {e}"

def find_match(user1_taste, user2_taste):
    """إيجاد فيلم مشترك يرضي ذوقين مختلفين"""
    if not client: return "عذراً، الوسيط الذكي غير متصل."
    prompt = f"""
    Act as a Movie Matchmaker. 
    Person A loves: "{user1_taste}".
    Person B loves: "{user2_taste}".
    Your Goal: Find the perfect "Intersection" movies that satisfy BOTH tastes.
    Output Format (Strictly in Arabic):
    1. Explain concisely why these movies work for both.
    2. Recommend 3 movies. Put English Titles in [Brackets].
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ: {e}"

def analyze_image_search(image_file):
    """المحقق البصري: تحليل الصورة واقتراح أفلام"""
    if not client: return "عذراً، المحقق البصري غير متصل."
    
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    
    prompt = """
    Analyze this image carefully. Describe the mood, lighting, and genre it represents.
    Then, recommend 3 movies or TV shows that have a very similar visual style or vibe.
    
    Format:
    1. A short description of the image vibe in Arabic.
    2. Recommendations with English titles inside [Brackets].
    """
    
    try:
        # استخدام الموديل الأحدث للرؤية
        completion = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.6,
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ أثناء تحليل الصورة: {e}"
