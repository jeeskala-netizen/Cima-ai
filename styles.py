import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
        
        /* الإعدادات العامة */
        html, body, [class*="st-"] {
            font-family: 'Cairo', sans-serif;
            direction: rtl; 
        }
        
        /* خلفية الصفحة */
        .stApp {
            background-color: #050505;
            color: #ffffff;
        }

        /* إخفاء القائمة الجانبية الافتراضية والقوائم العلوية المزعجة */
        [data-testid="stSidebar"], header, footer {
            display: none !important;
        }

        /* تنسيق العناوين */
        h1, h2, h3 {
            color: #E50914 !important; /* لون نتفليكس الأحمر */
            text-shadow: 0 0 10px rgba(229, 9, 20, 0.4);
            font-weight: 800;
        }

        /* تحسين شكل الأزرار */
        .stButton > button {
            background: linear-gradient(90deg, #E50914 0%, #B20710 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
        }

        /* شريط الأخبار المتحرك */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid #E50914;
            white-space: nowrap;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .ticker-item {
            display: inline-block;
            padding-right: 100%;
            animation: ticker 30s linear infinite;
            color: #ccc;
            font-size: 0.9rem;
        }
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(100%, 0, 0); } /* تعديل للحركة العربية */
        }

        /* كروت الأفلام */
        div[data-testid="caption"] {
            text-align: center;
            font-size: 0.9em;
            color: #aaa;
        }
        
        /* تخصيص الـ Tab العلوي */
        .nav-link-selected {
            background-color: #E50914 !important;
        }
        
        /* الصناديق والتحليل */
        .analysis-box {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            border-right: 5px solid #E50914;
            line-height: 1.8;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
