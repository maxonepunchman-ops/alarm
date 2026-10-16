import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(
    page_title="Real LooksMax AI (GPT-4o)",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 Real LooksMax AI: Экспертный анализ")
st.markdown("Настоящий разбор внешности с помощью мультимодальной нейросети GPT-4o.")

# Вставь свой платный ключ сюда в кавычки, либо оставь пустым, чтобы вводить в поле ниже
api_key = st.sidebar.text_input("Введи OpenAI API Key:", value="", type="password")

# Если хочешь зашить ключ намертво в код, просто раскомментируй строчку ниже и вставь ключ:
# api_key = "sk-proj-..."

uploaded_file = st.file_uploader("Загрузи чёткое фото лица (анфас)", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    # Отображаем фото
    st.image(uploaded_file, caption="Твоё фото для анализа", use_column_width=True)
    
    if st.button("🚀 Запустить глубокий анализ"):
        client = OpenAI(api_key=api_key)
        
        # Кодируем картинку в base64 для отправки в GPT-4o
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        
        prompt = """
        Ты — элитный эксперт по антропометрии, эстетике лица и луксмаксингу (Looksmaxing). 
        Проанализируй загруженное фотографию человека максимально честно, объективно и профессионально.

        Структура твоего ответа:
        1. 📊 **Текущие метрики и потенциал (оценка по шкале от 1 до 100)**:
           - Симметрия лица и пропорции третей
           - Качество кожи и тонус
           - Линия челюсти (Jawline) и подбородок
           - Общий уровень ухоженности и прическа

        2. 🔍 **Выявленные зоны роста (слабые стороны)**:
           - Укажи 3-4 реальные проблемы на фото (например: отечность, невыраженная челюсть из-за жировой прослойки, текстура кожи, асимметрия, несоответствие стрижки форме лица).

        3. 🎯 **Пошаговый план преображения (Looksmaxing Roadmap)**:
           - **Уровень 1 (1 Месяц / Softmaxing - быстрые фиксы):** Лимфодренаж, избавление от отеков (сон, осанка, вода, соль), уход за кожей, подбор правильной стрижки.
           - **Уровень 2 (3 Месяца / Тело и стиль):** Снижение процента жира (для проявления челюсти и скул), осанка, качественное питание.
           - **Уровень 3 (6+ Месяцев / Хардкор):** Работа с прикусом/ортодонтией, силовой тренинг для роста тестостерона и плотности мышц лица/тела.

        Пиши дерзко, мотивирующе, по делу, без банальной воды.
        """

        with st.spinner("🤖 GPT-4o сканирует геометрию лица и готовит разбор..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=1200,
                )
                
                result_text = response.choices[0].message.content
                st.success("Анализ успешно завершен!")
                st.markdown(result_text)

            except Exception as e:
                st.error(f"Ошибка при запросе к OpenAI API: {e}")

elif uploaded_file and not api_key:
    st.warning("⚠️ Введи свой OpenAI API Key в боковой панели слева, чтобы запустить нейросеть.")
