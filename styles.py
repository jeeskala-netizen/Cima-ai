import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
        }

        /* 🛑 إخفاء العناصر الإدارية وأشرطة Streamlit (الحل النهائي) */
        .stDeployButton {display: none !important;} /* زر Manage app */
        [data-testid="stToolbar"] {visibility: hidden !important;} /* الشريط العلوي للمطورين */
        [data-testid="stDecoration"] {display: none !important;} /* الخط الملون أعلى الصفحة */
        .viewerBadge_container__1QSob {display: none !important;} /* أيقونة المشاهدين */
        #MainMenu {visibility: hidden;} /* القائمة الرئيسية */
        footer {visibility: hidden;} /* الفوتر */
        header {visibility: hidden;} /* الهيدر */

        /* باقي التنسيقات كما هي... */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        section.main > div {
            padding-top: 2rem;
            max-width: 95% !important;
        }

        .nav-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(4px);
        }

        .stButton > button {
            background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(106, 17, 203, 0.5);
        }

        h1, h2 {
            background: -webkit-linear-gradient(#fff, #a18cd1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        
        div[data-baseweb="select"] > div {
            direction: rtl;
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True)
