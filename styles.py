import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
        
        /* 1. الأساسيات */
        html, body, [class*="st-"] {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }
        
        /* الخلفية */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
        }

        /* ============================================================
           🛑 منطقة الإخفاء التام (The Ultimate Clean-up) 🛑
           ============================================================ */
        
        /* 1. إخفاء الزر الأحمر (التاج) وشارة المشاهد في الزاوية اليمنى السفلى */
        /* نستهدف أي عنصر يحتوي اسمه على viewerBadge مهما تغيرت الأرقام بعده */
        div[class^="viewerBadge_container"], 
        div[class*="viewerBadge"], 
        .viewerBadge_container__1QSob {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* 2. إخفاء زر "Manage App" والأدوات العلوية */
        .stDeployButton, 
        [data-testid="stToolbar"], 
        [data-testid="stHeader"], 
        [data-testid="stDecoration"], 
        [data-testid="stStatusWidget"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 3. إخفاء القوائم الجانبية القديمة والهيدر/الفوتر */
        [data-testid="stSidebar"], 
        [data-testid="collapsedControl"], 
        #MainMenu, 
        footer, 
        header {
            display: none !important;
        }

        /* ============================================================ */

        /* 3. تنسيق القائمة العلوية (Nav Bar) */
        .nav-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(4px);
        }

        /* 4. تحسين العناصر */
        section.main > div {
            padding-top: 1rem !important;
            max-width: 95% !important;
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
