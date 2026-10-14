import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(
    page_title="Real LooksMax AI (Gemini)",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Real LooksMax AI (Gemini Vision)")
st.markdown("Анализ внешности с помощью бесплатной мультимодальной нейросети Gemini.")

# Получение API ключа
api_key = st.sidebar.text_input("Введи Gemini API Key (Google AI Studio):", type="password")

uploaded_file = st.file_uploader("Загрузи чёткое фото лица (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Твоё фото", use_column_width=True)
    
    if st.button("🚀 Проанализировать через Gemini"):
        genai.configure(api_key=api_key)
        # Используем модель с поддержкой мультимодальности (картинок)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Ты — эксперт по эстетике лица, антропометрии и луксмаксингу (Looksmaxing).
        Проанализируй загруженное фото человека и дай подробный, честный и конструктивный разбор.

        Структура ответа:
        1. 📊 **Оценка потенциала и текущих параметров (по шкале 1-100)**:
           - Симметрия и черты лица
           - Состояние кожи и чёткость овала
           - Линия челюсти (Jawline) и подбородок
           - Причёска и ухоженность

        2. 🔍 **Выявленные зоны роста (слабые стороны)**:
           - Назови 2-4 конкретные проблемы (например: отечность, нечеткий овал, проблемы с текстурой кожи, асимметрия прикуса/мимики, неподходящая стрижка).

        3. 🎯 **Индивидуальный пошаговый план улучшения (Looksmaxing Plan)**:
           - **Softmaxing (быстрые результаты за 1-3 месяца)**: уход за кожей, осанка, лимфодренаж, стрижка, фастинг/дефицит калорий для снижения % жира на лице.
           - **Hardmaxing / Долгосрок (3-12 месяцев)**: прикус/ортодонтия, жевательные мышцы, силовой тренинг, работа с пропорциями.

        Пиши четко, без лишней воды, дерзко, мотивирующе и по делу.
        """

        with st.spinner("🤖 Нейросеть Gemini сканирует фото..."):
            try:
                response = model.generate_content([prompt, image])
                st.success("Сканирование завершено!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ошибка: {e}")

elif uploaded_file and not api_key:
    st.warning("⚠️ Сначала введи бесплатный Gemini API Key в боковой панели слева.")
