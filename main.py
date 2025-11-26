import streamlit as st
from st_clickable_images import clickable_images
import config
import styles
import api

# --- 1. الإعدادات والتهيئة ---
st.set_page_config(page_title="AI Cinema Hub", page_icon="🍿", layout="wide")
styles.load_css()

# --- 📢 شريط المعلومات المتحرك (الجديد) ---
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker-item">
        🎬 مرحبًا بك في AI Cinema Hub! منصتك الشاملة التي تقترح عليك الأفلام والمسلسلات بناءً على التقييمات العالمية الدقيقة &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; 
        💡 معلومة ذكية: يمكنك استخدام "الذكاء الاصطناعي" للبحث عن أي فيلم بوصف القصة فقط! فعّل زر "العبقري" وجرب كتابة "فيلم عن سرقة بنك بذكاء" &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; 
        🌍 اكتشف الآن روائع السينما العالمية: الكورية، الأمريكية، العربية، التركية والمزيد!
    </div>
</div>
""", unsafe_allow_html=True)

# تهيئة الذاكرة
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'item_type' not in st.session_state: st.session_state.item_type = "movie"
if 'favorites' not in st.session_state: st.session_state.favorites = []
if 'current_analysis' not in st.session_state: st.session_state.current_analysis = None
if 'analyzed_id' not in st.session_state: st.session_state.analyzed_id = None

# دوال المفضلة
def is_favorite(id):
    return any(m['id'] == id for m in st.session_state.favorites)

def toggle_favorite(item, type):
    item['media_type'] = type 
    if is_favorite(item['id']):
        st.session_state.favorites = [m for m in st.session_state.favorites if m['id'] != item['id']]
        st.toast("🗑️ تم الحذف")
    else:
        st.session_state.favorites.append(item)
        st.toast("❤️ تم الإضافة")

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>AI CINEMA</div>", unsafe_allow_html=True)
    
    if st.session_state.selected_item:
        if st.button("⬅️ الرئيسية"):
            st.session_state.selected_item = None
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # اختيار النوع
    content_type = st.radio("نوع المحتوى:", ["أفلام 🎬", "مسلسلات 📺"], horizontal=True, label_visibility="collapsed")
    current_type = "movie" if content_type == "أفلام 🎬" else "tv"
    
    st.markdown("---")
    
    view_mode = st.radio("menu", ["🔍  الاستكشاف", "❤️  مكتبتي"], label_visibility="collapsed")
    st.markdown("---")
    
    # المتغيرات
    search_text = ""
    ai_mode = False
    category = "popular"
    region = None

    if view_mode == "🔍  الاستكشاف":
        st.markdown("<p style='color:#888; font-size:0.8rem;'>أدوات البحث</p>", unsafe_allow_html=True)
        ai_mode = st.toggle("تفعيل العبقري (AI)", value=False)
        search_text = st.text_input("search", placeholder=f"ابحث عن {content_type}...", label_visibility="collapsed")
        
        if not ai_mode:
            st.markdown("<br>", unsafe_allow_html=True)
            filter_type = st.radio("type", ["العالمية 🔥", "الدول 🌍"], horizontal=True, label_visibility="collapsed")
            
            if filter_type == "العالمية 🔥":
                opts = ["popular", "top_rated", "upcoming"] if current_type == "movie" else ["popular", "top_rated", "on_the_air"]
                labels = {"popular":"🔥 الرائج", "top_rated":"⭐ الأفضل", "upcoming":"📅 قريباً", "on_the_air":"📺 يُعرض الآن"}
                category = st.radio("cat", opts, format_func=lambda x: labels[x])
            else:
                opts = ["korea", "arabic", "turkey", "japan", "spain"]
                labels = {"korea": "🇰🇷 كورية", "arabic": "🕌 عربية", "turkey": "🇹🇷 تركية", "japan": "🇯🇵 أنيمي/ياباني", "spain": "🇪🇸 إسبانية"}
                region = st.radio("reg", opts, format_func=lambda x: labels[x])
    else:
        st.success(f"لديك {len(st.session_state.favorites)} في المفضلة")

# --- 3. منطقة العرض ---
if st.session_state.selected_item:
    # >>> عرض التفاصيل <<<
    m = st.session_state.selected_item
    title = m.get('title') or m.get('name') or m.get('original_name')
    org_title = m.get('original_title') or m.get('original_name')
    ctype = st.session_state.item_type
    
    st.image(config.BACKDROP_URL + (m['backdrop_path'] or ""), use_container_width=True)
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 20px;'>{org_title}</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    with c2:
        if m.get('poster_path'): st.image(config.IMAGE_URL + m['poster_path'], use_container_width=True)
        lbl = "💔 إزالة" if is_favorite(m['id']) else "❤️ إضافة"
        if st.button(lbl, use_container_width=True): toggle_favorite(m, ctype); st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎥 التريلر")
        t = api.get_trailer(m['id'], ctype)
        if t: st.video(t)
        else: st.info("غير متوفر")

    with c1:
        st.markdown(f"### 🧬 تحليل {content_type} الذكي")
        with st.spinner('🤔 جاري التحليل العميق...'):
            if st.session_state.analyzed_id != m['id']:
                st.session_state.current_analysis = api.generate_analysis(org_title, m['overview'], ctype)
                st.session_state.analyzed_id = m['id']
            
            analysis = st.session_state.current_analysis
            st.markdown(f"""
            <div style="direction: rtl; text-align: right; background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-right: 5px solid #E50914; font-size: 1.1rem; line-height: 1.8; color: #e0e0e0;">
                {analysis}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📝 القصة")
        st.markdown(f"""<div style="direction: rtl; text-align: right;">{m['overview']}</div>""", unsafe_allow_html=True)
        
        date = m.get('release_date') or m.get('first_air_date') or 'غير معروف'
        st.caption(f"📅 التاريخ: {date} | ⭐ التقييم: {m['vote_average']}")

else:
    # >>> عرض الشبكة <<<
    items = []
    
    if view_mode == "❤️  مكتبتي":
        st.markdown("<h1>مكتبتي ❤️</h1>", unsafe_allow_html=True)
        items = st.session_state.favorites
        if not items: st.info("المكتبة فارغة...")
    
    elif search_text:
        st.markdown(f"<h1>نتائج البحث: {search_text}</h1>", unsafe_allow_html=True)
        items = api.semantic_search(search_text) if ai_mode else api.search_tmdb(search_text, current_type)
        if not items: st.warning("لا توجد نتائج.")
    
    else:
        title_text = f"قائمة {content_type}"
        if region: title_text += f" ({region})"
        st.markdown(f"<h1>{title_text}</h1>", unsafe_allow_html=True)
        
        if current_type == "movie":
            items = api.fetch_movies(category, region)
        else:
            items = api.fetch_tv_shows(category, region)

    if items:
        imgs, names, indices = [], [], []
        for i, item in enumerate(items):
            if item.get('poster_path'):
                imgs.append(config.IMAGE_URL + item['poster_path'])
                names.append(item.get('title') or item.get('name'))
                indices.append(i)
        
        if imgs:
            clicked = clickable_images(
                imgs, titles=names,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "gap": "20px"},
                img_style={"cursor": "pointer", "border-radius": "12px", "width": "180px", "transition": "transform 0.4s", "box-shadow": "0 10px 30px rgba(0,0,0,0.5)"},
                key=f"grid_{content_type}_{category}_{region}"
            )
            
            if clicked > -1:
                selected = items[indices[clicked]]
                st.session_state.selected_item = selected
                st.session_state.item_type = selected.get('media_type', current_type)
                st.rerun()