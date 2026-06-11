import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة الرسمية للموقع
st.set_page_config(page_title="Raqawi Pro AI", page_icon="🤖", layout="centered")

# التصميم الواجهة والترحيب بالزوار
st.title("🤖 Raqawi Pro")
st.subheader("بوابتك الذكية المدعومة بتقنيات Google AI المتقدمة")
st.write("مرحباً بك في Raqawi Pro. يمكنك البدء في اختبار وتجربة ميزات الذكاء الاصطناعي هنا.")

# شريط جانبي لإدخال الـ API Key لتأمين موقعك أو تجربة مفتاحك الخاص
with st.sidebar:
    st.header("⚙️ إعدادات الربط")
    api_key = st.text_input("أدخل مفتاح Google API الخاص بك:", type="password")
    st.info("يمكنك الحصول على المفتاح مجاناً من Google AI Studio.")

# التحقق من وجود المفتاح وبدء الربط مع ذكاء جوجل
if api_key:
    # تهيئة مكتبة جوجل بالمفتاح المدخل
    genai.configure(api_key=api_key)
    
    # استخدام أحدث نموذج متاح
    model = genai.GenerativeModel('gemini-1.5-flash')

    # إنشاء ذاكرة للمحادثة في الموقع (Session State)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة في صندوق المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال سؤال أو أمر جديد من المستخدم
    if prompt := st.chat_input("اسأل ذكاء Raqawi Pro عن أي شيء..."):
        # عرض سؤال المستخدم فوراً
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # إرسال الطلب إلى ذكاء جوجل وجلب الرد
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("جاري التفكير والتوليد..."):
                try:
                    response = model.generate_content(prompt)
                    full_response = response.text
                    message_placeholder.markdown(full_response)
                    # حفظ الرد في الذاكرة
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بجوجل: {e}")
else:
    st.warning("⚠️ يرجى إدخال مفتاح Google API في الشريط الجانبي لتفعيل الموقع وبدء الاستخدام.")
