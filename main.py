import streamlit as st
from st_clickable_images import clickable_images
from streamlit_option_menu import option_menu
import config
import styles
import api
import re 

# --- 1. الإعدادات ---
st.set_page_config(page_title="AI Cinema Hub", page_icon="🔮", layout="wide")
styles.load_css()

# --- Router ---
def update_url(page_name):
    st.session_state.page = page_name
    st.query_params["page"] = page_name

current_query = st.query_params.get("page", "chat_home")

# --- State ---
if 'page' not in st.session_state: st.session_state.page = current_query
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = None
if 'favorites' not in st.session_state: st.session_state.favorites = []
if 'content_type' not in st.session_state: st.session_state.content_type = "movie"
if 'previous_nav' not in st.session_state: st.session_state.previous_nav = "الرئيسية"
if 'dna_result' not in st.session_state: st.session_state.dna_result = None
if 'match_result' not in st.session_state: st.session_state.match_result = None
if 'visual_result' not in st.session_state: st.session_state.visual_result = None

if st.session_state.page != current_query: st.session_state.page = current_query

# الترحيب
welcome_msg = "أهلاً بك! 👋 أنا دليلك السينمائي الذكي. أخبرني بمزاجك وسأقترح عليك روائع تناسب ذوقك! 🎥✨"
if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

def get_welcome_msg(persona):
    if "الناقد" in persona: return "أهلاً. أنا الناقد السينمائي. هات ما عندك بذكاء. 🧐"
    elif "الجوكر" in persona: return "لماذا أنت جاد هكذا؟ 🤡 دعنا نجد فيلماً يضحكنا!"
    elif "المتحمس" in persona: return "يا هلااا! 🔥 مستعد لأقوى الاقتراحات؟ 🚀🤩"
    else: return welcome_msg

# --- 2. الشريط العلوي (Top Navigation) ---
st.markdown("<h1 style='margin-bottom: 10px;'>AI CINEMA 🔮</h1>", unsafe_allow_html=True)

default_idx = 0
if st.session_state.page == "chat_home": default_idx = 0
elif st.session_state.page == "browse" and st.session_state.content_type == "movie": default_idx = 1
elif st.session_state.page == "browse" and st.session_state.content_type == "tv": default_idx = 2
elif st.session_state.page == "visual_detective": default_idx = 3
elif st.session_state.page == "dna_analysis": default_idx = 4
elif st.session_state.page == "matchmaker": default_idx = 5
elif st.session_state.page == "library": default_idx = 6

selected_nav = option_menu(
    menu_title=None, 
    options=["الرئيسية", "أفلام", "مسلسلات", "محقق بصري", "تحليل DNA", "توحيد السهرة", "مفضلتي"],
    icons=["chat-quote", "film", "tv", "camera", "fingerprint", "people-arrows", "heart"],
    default_index=default_idx,
    orientation="horizontal", 
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.05)", "border-radius": "15px"},
        "icon": {"color": "#f0e68c", "font-size": "14px"}, 
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#4b0082", "color": "white"},
        "nav-link-selected": {"background-color": "#6a11cb", "color": "white", "box-shadow": "0px 0px 15px rgba(106, 17, 203, 0.5)"},
    }
)

# --- 3. التوجيه ---
if selected_nav != st.session_state.previous_nav:
    st.session_state.previous_nav = selected_nav
    if selected_nav == "الرئيسية": update_url("chat_home"); st.rerun()
    elif selected_nav == "أفلام": st.session_state.content_type = "movie"; update_url("browse"); st.rerun()
    elif selected_nav == "مسلسلات": st.session_state.content_type = "tv"; update_url("browse"); st.rerun()
    elif selected_nav == "محقق بصري": update_url("visual_detective"); st.rerun()
    elif selected_nav == "تحليل DNA": update_url("dna_analysis"); st.rerun()
    elif selected_nav == "توحيد السهرة": update_url("matchmaker"); st.rerun()
    elif selected_nav == "مفضلتي": update_url("library"); st.rerun()

st.markdown("---")

# --- 4. الدوال المساعدة ---
def extract_and_display_media(text, message_index):
    st.markdown(text)
    matches = re.findall(r'\[(.*?)\]', text)
    if matches:
        st.markdown("---")
        st.caption("🎬 المحتوى المقترح:")
        cols = st.columns(len(matches))
        for i, movie_name in enumerate(matches):
            results = api.search_tmdb(movie_name)
            if results:
                item = results[0]
                poster = item.get('poster_path')
                if poster:
                    with cols[i % 3]:
                        st.image(config.IMAGE_URL + poster, use_container_width=True)
                        st.caption(f"**{item.get('title') or item.get('name')}**")
                        btn_key = f"btn_{item['id']}_msg{message_index}_{i}"
                        if st.button(f"تفاصيل ⬅️", key=btn_key, use_container_width=True):
                            st.session_state.selected_movie = item
                            update_url("details"); st.rerun()

def show_grid(items):
    if not items: st.warning("لا توجد نتائج."); return
    images, titles, valid_items = [], [], []
    for item in items:
        if item.get('poster_path'):
            images.append(config.IMAGE_URL + item['poster_path'])
            titles.append(item.get('title') or item.get('name'))
            valid_items.append(item)
    if images:
        clicked = clickable_images(images, titles=titles, div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "gap": "15px", "padding": "10px"}, img_style={"cursor": "pointer", "border-radius": "12px", "width": "140px", "box-shadow": "0 5px 15px rgba(0,0,0,0.5)", "transition": "transform 0.3s"}, key=f"grid_{st.session_state.content_type}_{len(items)}")
        if clicked > -1: st.session_state.selected_movie = valid_items[clicked]; update_url("details"); st.rerun()

def show_details(item):
    if st.button("🔙 عودة للقائمة", key="back_btn_details"):
        if st.session_state.previous_nav == "الرئيسية": update_url("chat_home")
        elif st.session_state.previous_nav == "محقق بصري": update_url("visual_detective")
        elif st.session_state.previous_nav == "تحليل DNA": update_url("dna_analysis")
        elif st.session_state.previous_nav == "توحيد السهرة": update_url("matchmaker")
        else: update_url("browse")
        st.rerun()
        
    title = item.get('title') or item.get('name')
    backdrop = item.get('backdrop_path'); poster = item.get('poster_path')
    
    if backdrop: st.image(config.BACKDROP_URL + backdrop, use_container_width=True)
    st.markdown(f"<h1 style='text-align:center; text-shadow: 0 0 20px #6a11cb;'>{title}</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if poster: st.image(config.IMAGE_URL + poster, use_container_width=True)
        st.markdown("##### 📺 متوفر على:")
        providers = api.get_watch_providers(item['id'], 'movie' if item.get('title') else 'tv')
        if providers:
            p_cols = st.columns(len(providers))
            for i, prov in enumerate(providers):
                if prov.get('logo_path'):
                    with p_cols[i]: st.image(config.IMAGE_URL + prov['logo_path'], width=50)
        else: st.caption("غير متوفر رقمياً.")
        st.markdown("---")
        is_fav = any(f['id'] == item['id'] for f in st.session_state.favorites)
        if st.button("💔 حذف" if is_fav else "❤️ مفضلة", use_container_width=True):
            if is_fav: st.session_state.favorites = [f for f in st.session_state.favorites if f['id'] != item['id']]; st.toast("تم الحذف")
            else: item['media_type'] = 'movie' if item.get('title') else 'tv'; st.session_state.favorites.append(item); st.toast("تمت الإضافة"); st.rerun()
            
    with c2:
        st.markdown("### 📝 القصة")
        st.write(item.get('overview', 'لا يوجد وصف.'))
        trailer = api.get_trailer(item['id'], 'movie' if item.get('title') else 'tv')
        if trailer: st.video(trailer)

# --- 5. الصفحات ---

# 1. شات (تم تعديل الزر هنا 🛠️)
if st.session_state.page == "chat_home":
    with st.container(border=True):
        col_set, col_btn = st.columns([3, 1])
        with col_set: 
            selected_persona = st.radio("الشخصية:", ["الصديق الناصح 🤝", "الناقد القاسي 🧐", "الجوكر الساخر 🤡", "المتحمس (Fanboy) 🤩"], horizontal=True, label_visibility="collapsed")
        with col_btn: 
            st.markdown("<br>", unsafe_allow_html=True)
            # ✅ الزر الجديد: أيقونة جميلة ونص واضح
            if st.button("🎭 تغيير الشخصية", use_container_width=True): 
                st.session_state.messages = []
                new_welcome = get_welcome_msg(selected_persona)
                st.session_state.messages.append({"role": "assistant", "content": new_welcome})
                st.rerun()
    
    with st.container():
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "system": continue
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant": extract_and_display_media(msg["content"], i)
                else: st.write(msg["content"])
    if prompt := st.chat_input("اكتب هنا.."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner(f"{selected_persona.split()[0]} يكتب..."):
                response = api.chat_with_ai_formatted(st.session_state.messages, selected_persona)
                extract_and_display_media(response, len(st.session_state.messages))
                st.session_state.messages.append({"role": "assistant", "content": response})

# 2. المحقق البصري
elif st.session_state.page == "visual_detective":
    st.markdown("<h2 style='text-align: center;'>🕵️ المحقق البصري</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("ارفع صورة (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="الصورة", use_container_width=True)
            if st.button("🔍 ابدأ التحليل", use_container_width=True):
                with st.spinner("جاري التحليل..."): st.session_state.visual_result = api.analyze_image_search(uploaded_file)
    with col2:
        if st.session_state.visual_result: st.success("تم!"); extract_and_display_media(st.session_state.visual_result, 777)

# 3. DNA
elif st.session_state.page == "dna_analysis":
    st.markdown("<h2 style='text-align: center;'>🧬 تحليل الحمض النووي</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        m1 = st.text_input("فيلم 1 ⭐")
        m2 = st.text_input("فيلم 2 ⭐⭐")
        m3 = st.text_input("فيلم 3 ⭐⭐⭐")
        if st.button("🔍 حلل شخصيتي", use_container_width=True):
            if m1 and m2 and m3:
                with st.spinner("جاري التحليل..."): st.session_state.dna_result = api.analyze_dna([m1, m2, m3])
    with c2:
        if st.session_state.dna_result: st.success("النتيجة:"); extract_and_display_media(st.session_state.dna_result, 999)

# 4. توحيد السهرة
# 4. توحيد السهرة (Movie Matchmaker)
elif st.session_state.page == "matchmaker":
    # العنوان الرئيسي
    st.markdown("<h1 style='text-align: center; color: #E50914;'>⚖️ توحيد السهرة</h1>", unsafe_allow_html=True)
    
    # --- الإضافة الجديدة: الشرح التوضيحي ---
    st.markdown("""
    <div style='text-align: center; color: #ccc; margin-bottom: 30px; font-size: 1.1rem;'>
    مختلفين على فيلم السهرة؟ 🤔<br>
    لا داعي للنقاش! اكتب نوع الأفلام الذي يحبه <b>الطرف الأول</b>، والنوع الذي يحبه <b>الطرف الثاني</b>، 
    وسيقوم الذكاء الاصطناعي بإيجاد <b>"الحل الوسط"</b> العبقري الذي يرضي الجميع! 🍿🤝
    </div>
    """, unsafe_allow_html=True)
    # ---------------------------------------

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 👤 الطرف الأول")
        u1 = st.text_input("ماذا يحب؟", placeholder="مثال: أفلام رعب، زومبي، أكشن...")
    with c2:
        st.markdown("### 👤 الطرف الثاني")
        u2 = st.text_input("ماذا يحب؟", placeholder="مثال: أفلام رومانسية، كوميديا، دراما...")
    
    st.markdown("<br>", unsafe_allow_html=True) # مسافة
    
    if st.button("✨ جد لنا الحل العبقري!", use_container_width=True):
        if u1 and u2:
            with st.spinner("جاري تحليل الأذواق والبحث عن نقطة الالتقاء... 🔄"):
                st.session_state.match_result = api.find_match(u1, u2)
        else:
            st.warning("⚠️ يرجى كتابة تفضيلات الطرفين أولاً!")

    if st.session_state.match_result:
        st.success("🎉 وجدنا الحل المناسب لكم!")
        extract_and_display_media(st.session_state.match_result, 888)

# 5. التفاصيل
elif st.session_state.page == "details":
    if st.session_state.selected_movie: show_details(st.session_state.selected_movie)
    else: update_url("chat_home"); st.rerun()

# 6. التصفح
elif st.session_state.page == "browse":
    st.markdown(f"<h2 style='text-align: center;'>تصفح {'الأفلام' if st.session_state.content_type == 'movie' else 'المسلسلات'}</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1: sort_by = st.selectbox("ترتيب:", ["الأكثر شهرة", "الأعلى تقييماً", "يعرض الآن"]); cat_map = {"الأكثر شهرة": "popular", "الأعلى تقييماً": "top_rated", "يعرض الآن": "now_playing" if st.session_state.content_type=="movie" else "on_the_air"}
    with c2: search = st.text_input("بحث...")
    if search: res = api.search_tmdb(search, st.session_state.content_type)
    else: res = api.fetch_content(st.session_state.content_type, cat_map[sort_by])
    show_grid(res)

# 7. المكتبة
elif st.session_state.page == "library":
    st.markdown("<h2 style='text-align: center;'>❤️ مفضلاتي</h2>", unsafe_allow_html=True)
    show_grid(st.session_state.favorites)
