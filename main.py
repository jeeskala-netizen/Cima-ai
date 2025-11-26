import streamlit as st
from st_clickable_images import clickable_images
from streamlit_option_menu import option_menu
import config
import styles
import api

# --- 1. الإعدادات والتهيئة ---
st.set_page_config(page_title="AI Cinema Hub", page_icon="🎬", layout="wide")
styles.load_css()

# تهيئة الذاكرة (Session State) لضمان عدم ضياع البيانات عند التفاعل
if 'page' not in st.session_state: st.session_state.page = 'home' # home, details, library
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = None
if 'favorites' not in st.session_state: st.session_state.favorites = []
if 'content_type' not in st.session_state: st.session_state.content_type = "movie" # movie or tv
if 'search_mode' not in st.session_state: st.session_state.search_mode = False

# --- 2. الشريط العلوي (بديل القائمة الجانبية) ---

# شريط الأخبار المتحرك
st.markdown("""
<div class="ticker-wrap">
<div class="ticker-item">
✨ AI Cinema Hub: بوابتك الذكية لعالم السينما. جرب البحث بالذكاء الاصطناعي: "أريد فيلماً يشبه Inception لكن بنهاية سعيدة" ✨
</div></div>
""", unsafe_allow_html=True)

# القائمة العلوية الاحترافية
selected_nav = option_menu(
    menu_title=None,
    options=["أفلام", "مسلسلات", "المفضلة", "بحث ذكي"],
    icons=["film", "tv", "heart", "stars"],
    default_index=0 if st.session_state.content_type == "movie" and not st.session_state.search_mode else 1,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#E50914", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "white"},
        "nav-link-selected": {"background-color": "#E50914", "color": "white"},
    }
)

# منطق التوجيه بناءً على القائمة العلوية
if selected_nav == "أفلام":
    st.session_state.content_type = "movie"
    st.session_state.
