# config.py
import streamlit as st

# نحاول قراءة المفاتيح من خزانة أسرار Streamlit
# إذا لم نجدها (يعني نحن على جهازك المحلي)، نستخدم المفاتيح المباشرة

try:
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # هذه المفاتيح احتياطية للعمل على جهازك فقط (Localhost)
    # لكن عند الرفع، السيرفر سيستخدم الـ secrets
    TMDB_API_KEY = "92a2bfcd6e2b85e41ca046e16c94ac03"
    GROQ_API_KEY = "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"

# روابط النظام
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_URL = "https://image.tmdb.org/t/p/original"
