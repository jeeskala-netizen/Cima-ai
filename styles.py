import streamlit as st
import streamlit.components.v1 as components # مكتبة جديدة ضرورية

def load_css():
    # 1. التنسيقات الجمالية (الألوان والخطوط)
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

        /* تنسيق القائمة العلوية */
        .nav-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(4px);
        }

        /* الأزرار */
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

        /* العناوين */
        h1, h2 {
            background: -webkit-linear-gradient(#fff, #a18cd1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        
        /* إخفاء القوائم الجانبية */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* تعديل المسافات */
        section.main > div {
            padding-top: 1rem !important;
            max-width: 95% !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. السلاح السري: كود جافاسكريبت لحذف شعارات Streamlit نهائياً
    # هذا الكود يعمل خارج نطاق CSS العادي ويجبر العناصر على الاختفاء
    components.html("""
        <script>
            // وظيفة تحاول العثور على العناصر المزعجة وحذفها
            function removeStreamlitElements() {
                const selectors = [
                    'footer', 
                    'header[data-testid="stHeader"]',
                    '.stAppDeployButton', 
                    '[data-testid="stDecoration"]',
                    '[data-testid="stStatusWidget"]',
                    'div[class^="viewerBadge"]' // استهداف الزر الأحمر (التاج)
                ];
                
                selectors.forEach(selector => {
                    const elements = window.parent.document.querySelectorAll(selector);
                    elements.forEach(el => {
                        el.style.display = 'none';
                        el.style.visibility = 'hidden';
                        el.innerHTML = ''; // تفريغ المحتوى لضمان عدم ظهوره
                    });
                });
            }

            // تشغيل الحذف فوراً ثم تكراره للتأكد (لأن الزر الأحمر يتأخر في الظهور)
            removeStreamlitElements();
            setInterval(removeStreamlitElements, 500); // كرر المحاولة كل نصف ثانية
        </script>
    """, height=0, width=0)
