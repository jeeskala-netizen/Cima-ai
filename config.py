import streamlit as st
import os

# هذه الطريقة هي الأكثر أماناً واستقراراً
# ستبحث أولاً في st.secrets، وإذا لم تجدها (لأي سبب) لن ينهار التطبيق فوراً
try:
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    # هذا يظهر فقط إذا نسيت ملف secrets.toml محلياً
    st.error("ملف الأسرار (secrets.toml) مفقود! يرجى إعداده.")
    st.stop()
except KeyError as e:
    # هذا يظهر إذا كان الاسم في الملف مختلفاً عن الكود
    st.error(f"المفتاح {e} غير موجود في ملف الأسرار.")
    st.stop()
