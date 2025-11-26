import streamlit as st
from st_clickable_images import clickable_images
from streamlit_option_menu import option_menu # تأكد من تثبيت هذه المكتبة
import config
import styles
import api

# --- 1. الإعدادات الأولية ---
st.set_page_config(page_title="AI Cinema Hub", page_icon="🎬", layout="wide")
styles.load_css()

# تهيئة الذاكرة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'home' # home, details
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = None
if 'favorites' not in st.session_state: st.session_state.favorites = []
if 'content_type' not in st.session_state: st.session_state.content_type = "movie" # movie or tv

# --- 2. الشريط العلوي (بديل القائمة الجانبية) ---
# شريط الأخبار
st.markdown("""
<div class="ticker-wrap">
<div class="ticker-item">
✨ AI Cinema Hub: بوابتك الذكية لعالم السينما. جرب البحث بالذكاء الاصطناعي: "أريد فيلماً يشبه Inception لكن بنهاية سعيدة" ✨
</div></div>
""", unsafe_allow_html=True)

# القائمة العلوية
selected_nav = option_menu(
    menu_title=None,
    options=["أفلام", "مسلسلات", "المفضلة", "بحث ذكي"],
    icons=["film", "tv", "heart", "stars"],
    default_index=0 if st.session_state.content_type == "movie" else 1,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#333"},
        "nav-link-selected": {"background-color": "#E50914"},
    }
)

# تحديث الحالة بناءً على القائمة العلوية
if selected_nav == "أفلام":
    st.session_state.content_type = "movie"
    if st.session_state.page == 'library': st.session_state.page = 'home' # إعادة تعيين إذا كنا في المكتبة
elif selected_nav == "مسلسلات":
    st.session_state.content_type = "tv"
elif selected_nav == "المفضلة":
    st.session_state.page = "library"

# --- 3. المنطق الرئيسي للعرض ---

def show_details(item):
    """عرض تفاصيل الفيلم/المسلسل"""
    # زر عودة ذكي لا يعيد تحميل الصفحة بالكامل
    if st.button("🔙 عودة للقائمة", key="back_btn"):
        st.session_state.selected_movie = None
        st.session_state.page = "home"
        st.rerun()

    # جلب المعلومات
    title = item.get('title') or item.get('name')
    org_title = item.get('original_title') or item.get('original_name')
    backdrop = item.get('backdrop_path')
    poster = item.get('poster_path')
    
    # عرض الغلاف الخلفي الكبير
    if backdrop:
        st.image(config.BACKDROP_URL + backdrop, use_container_width=True)
    
    st.markdown(f"<h1 style='text-align: center'>{title}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if poster:
            st.image(config.IMAGE_URL + poster, use_container_width=True)
        
        # زر المفضلة
        is_fav = any(f['id'] == item['id'] for f in st.session_state.favorites)
        if st.button("💔 إزالة من المفضلة" if is_fav else "❤️ إضافة للمفضلة"):
            if is_fav:
                st.session_state.favorites = [f for f in st.session_state.favorites if f['id'] != item['id']]
                st.toast("تم الحذف من مكتبتك")
            else:
                item['media_type'] = st.session_state.content_type
                st.session_state.favorites.append(item)
                st.toast("تمت الإضافة لمكتبتك")
            st.rerun()

    with col2:
        # التريلر
        trailer_url = api.get_trailer(item['id'], st.session_state.content_type)
        if trailer_url:
            st.video(trailer_url)
        else:
            st.info("عذراً، لا يوجد إعلان تشويقي متاح.")
            
        st.markdown("### 📝 القصة")
        st.write(item.get('overview', 'لا يتوفر وصف حالياً.'))
        
        st.markdown("---")
        # التحليل الذكي
        if st.button("🤖 اطلب رأي الناقد الذكي"):
            with st.spinner("جاري تحليل السيناريو وكشف الثغرات..."):
                analysis = api.generate_analysis(org_title, item.get('overview'), st.session_state.content_type)
                st.markdown(f"<div class='analysis-box'>{analysis}</div>", unsafe_allow_html=True)

def show_grid(items):
    """عرض شبكة الأفلام"""
    if not items:
        st.warning("لا توجد نتائج لعرضها.")
        return

    images = []
    titles = []
    
    for item in items:
        path = item.get('poster_path')
        if path:
            images.append(config.IMAGE_URL + path)
            titles.append(item.get('title') or item.get('name'))
    
    # عرض الصور القابلة للنقر
    clicked = clickable_images(
        images, 
        titles=titles,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "gap": "20px", "padding": "20px"},
        img_style={"cursor": "pointer", "border-radius": "10px", "transition": "transform 0.3s", "width": "150px", "box-shadow": "0 5px 15px black"},
    )
    
    if clicked > -1:
        # عند النقر، نحدث الحالة ونعيد التحميل لعرض التفاصيل
        st.session_state.selected_movie = items[clicked]
        st.session_state.page = "details"
        st.rerun()

# --- 4. التحكم في توجيه الصفحات ---

if st.session_state.page == "details" and st.session_state.selected_movie:
    show_details(st.session_state.selected_movie)

elif st.session_state.page == "library":
    st.title("📂 مكتبتي الخاصة")
    if not st.session_state.favorites:
        st.info("مكتبتك فارغة حالياً.")
    else:
        show_grid(st.session_state.favorites)

else: # الصفحة الرئيسية (Home)
    # خيارات الفلترة تظهر فقط في الرئيسية
    if selected_nav == "بحث ذكي":
        st.title("🧠 البحث الدلالي بالذكاء الاصطناعي")
        query = st.text_input("اوصف الفيلم الذي في خيالك...", placeholder="مثال: فيلم عن سرقة بنك بذكاء شديد ونهاية صادمة")
        if query:
            with st.spinner("الذكاء الاصطناعي يبحث لك..."):
                results = api.semantic_search_ai(query)
                show_grid(results)
    else:
        # أدوات التحكم (فلاتر) في الأعلى
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.session_state.content_type == "movie":
                filter_opt = st.selectbox("تصنيف:", ["الرائج", "الأعلى تقييماً", "قريباً"], label_visibility="collapsed")
                cat_map = {"الرائج": "popular", "الأعلى تقييماً": "top_rated", "قريباً": "upcoming"}
            else:
                filter_opt = st.selectbox("تصنيف:", ["الرائج", "الأعلى تقييماً", "يعرض الآن"], label_visibility="collapsed")
                cat_map = {"الرائج": "popular", "الأعلى تقييماً": "top_rated", "يعرض الآن": "on_the_air"}
            
            region_opt = st.selectbox("الدولة:", ["الكل", "كوريا", "تركيا", "الهند", "العرب", "اليابان (أنيمي)"], label_visibility="collapsed")
            reg_map = {"الكل": None, "كوريا": "korea", "تركيا": "turkey", "الهند": "india", "العرب": "arabic", "اليابان (أنيمي)": "japan"}

        with c2:
            search_query = st.text_input("بحث سريع...", label_visibility="collapsed", placeholder=f"ابحث في {selected_nav}...")

        # منطق جلب البيانات
        if search_query:
            results = api.search_tmdb(search_query, st.session_state.content_type)
        else:
            category = cat_map[filter_opt]
            region = reg_map[region_opt]
            results = api.fetch_content(st.session_state.content_type, category, region)
        
        show_grid(results)
