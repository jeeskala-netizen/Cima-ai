import streamlit as st

# --- 1. قسم المفاتيح (Secrets) ---
try:
    # محاولة جلب المفاتيح من السيكريت
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # قيم احتياطية (تظهر فقط عند عدم وجود ملف secrets)
    # لا تضع مفاتيحك الحقيقية هنا عند الرفع على GitHub للأمان
    TMDB_API_KEY = "" 
    GROQ_API_KEY = ""

# --- 2. قسم الروابط الثابتة (هام جداً) ---
# يجب أن تكون هذه الأسطر هنا في الخارج، لا تضعها داخل try
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_URL = "https://image.tmdb.org/t/p/original"
