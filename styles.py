import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
        
        /* 1. إعدادات الصفحة (إصلاح المشكلة) */
        /* نترك الاتجاه العام LTR لكي تعمل القائمة، لكن نجبر النصوص على RTL */
        html, body {
            font-family: 'Cairo', sans-serif; 
            background-color: #050505 !important; 
            color: #ffffff !important;
        }

        /* حاوية التطبيق الرئيسية والقائمة الجانبية نجعل محتواها عربي */
        .stApp, section[data-testid="stSidebar"] {
            direction: rtl; 
            text-align: right;
        }

        /* 2. القائمة الجانبية الزجاجية (عادت لليسار لتعمل بامتياز) */
        section[data-testid="stSidebar"] {
            background-image: linear-gradient(160deg, #120002 0%, #000000 100%) !important;
            border-right: 1px solid rgba(229, 9, 20, 0.2); /* الحد أصبح يمين */
            border-left: none;
            box-shadow: 10px 0 30px rgba(0,0,0,0.8);
        }
        
        /* الشعار */
        .sidebar-logo {
            font-size: 2.5rem; text-align: center; color: #fff; font-weight: 900; 
            margin-bottom: 40px; letter-spacing: 2px;
            text-shadow: 0 0 10px #E50914, 0 0 20px #E50914;
            border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px;
        }

        /* 3. البطاقات والخيارات */
        div[role="radiogroup"] > label > div:first-of-type { display: none; }
        div[role="radiogroup"] > label {
            background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 12px;
            margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.4s; display: flex; justify-content: center;
        }
        div[role="radiogroup"] > label:hover {
            background: linear-gradient(270deg, rgba(229, 9, 20, 0.2) 0%, rgba(0,0,0,0) 100%);
            border-right: 5px solid #E50914; border-left: none;
            transform: translateX(-8px);
        }

        /* 4. حقل البحث */
        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.05) !important; color: white !important;
            border: 1px solid #333 !important; border-radius: 50px !important;
            padding: 10px 20px !important; transition: all 0.3s; text-align: right;
        }
        .stTextInput > div > div > input:focus {
            border-color: #E50914 !important; box-shadow: 0 0 15px rgba(229, 9, 20, 0.4) !important;
        }

        /* 5. الأزرار */
        .stButton > button {
            background: linear-gradient(90deg, #E50914 0%, #83050b 100%); color: white;
            border: none; border-radius: 8px; padding: 0.6rem 1.2rem; font-weight: 800;
            width: 100%; transition: all 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #ff1f2c 0%, #b30912 100%);
            box-shadow: 0 0 20px rgba(229, 9, 20, 0.6); transform: scale(1.02);
        }

        /* 6. العناوين */
        h1 { 
            background: -webkit-linear-gradient(left, #E50914, #ffffff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 900 !important; font-size: 3rem !important;
        }
        .stToggle label { color: #E50914 !important; font-weight: bold; }

        /* 7. شريط الأخبار المتحرك */
        .ticker-wrap {
            direction: ltr; /* اتجاه الحاوية LTR ليعمل الأنيميشن */
            width: 100%; overflow: hidden; 
            background: linear-gradient(90deg, #500000 0%, #E50914 50%, #500000 100%);
            padding: 12px 0; margin-bottom: 25px; border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }
        .ticker-item {
            display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite;
            color: #ffffff; font-weight: 700; font-size: 1.1rem; 
            direction: rtl; /* النص بداخله عربي */
        }
        @keyframes ticker {
            0% { transform: translate3d(-100%, 0, 0); }
            100% { transform: translate3d(100%, 0, 0); }
        }

        /* 8. أيقونة المنزل 3D */
        section[data-testid="stSidebar"] .stButton:first-of-type button {
            background: linear-gradient(145deg, #E50914, #a30000) !important;
            color: transparent !important; width: 70px !important; height: 70px !important;
            border-radius: 50% !important; padding: 0 !important; margin: 0 auto 20px auto !important;
            display: flex !important; justify-content: center; align-items: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.6), inset 2px 2px 5px rgba(255,255,255,0.3), inset -3px -3px 8px rgba(0,0,0,0.5) !important;
            border: 2px solid #ff3333 !important; position: relative;
        }
        section[data-testid="stSidebar"] .stButton:first-of-type button::after {
            content: "🏠"; font-size: 35px; color: white; position: absolute;
        }
        section[data-testid="stSidebar"] .stButton:first-of-type button:hover {
            transform: translateY(-5px) scale(1.1) !important;
            background: linear-gradient(145deg, #ff1f2c, #c40000) !important;
        }
        
        /* تصحيحات إضافية */
        .stRadio div[role="radiogroup"] { flex-direction: column; align-items: stretch; }
        
        /* زر إغلاق القائمة يعود لمكانه الصحيح */
        button[kind="header"] { float: right; }
    </style>
    """, unsafe_allow_html=True)
