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

# Вставь свой платный ключ в кавычки ниже (например, api_key = "sk-proj-..."),
# либо вводи его в боковой панели сайта.
api_key = st.sidebar.text_input("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", value="", type="password")

uploaded_file = st.file_uploader("Загрузи чёткое фото лица (анфас)", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    st.image(uploaded_file, caption="Твоё фото для анализа", use_column_width=True)
    
    if st.button("🚀 Запустить глубокий анализ"):
        client = OpenAI(api_key=api_key)
        
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        
        prompt = """
        Проанализируй этот фотоснимок с точки зрения фотогеничности, света и визуального стиля парня на фото. 
        Дай детальный разбор его внешних данных (симметрия, структура нижней челюсти и овала лица, текстура кожи, стрижка).

        Раздели ответ на блоки:
        1. 📊 Оценка текущих параметров и сильных сторон.
        2. 🔍 Слабые зоны (что портит кадр или требует прокачки: отёки, осанка, качество кожи, плотность жировой прослойки).
        3. 🎯 Программа преображения (Looksmaxing) на 1 месяц, 3 месяца и 6 месяцев (уход, лимфодренаж, осанка, спорт, стиль).

        Пиши дерзко, по делу, без лишней воды и банальных отказов, это развлекательный гид по стилю.
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
