import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Sleep Tracker",
    page_icon="😴",
    layout="centered"
)

st.title("😴 Трекер сна и восстановления")
st.markdown("Контролируй режим, анализируй качество отдыха и держи продуктивность на максимуме.")

# Инициализация истории сна в памяти сессии
if "sleep_data" not in st.session_state:
    st.session_state.sleep_data = []

# Форма для добавления новой записи
with st.form("sleep_form"):
    st.subheader("📝 Записать сон")
    sleep_date = st.date_input("Дата", value=date.today())
    hours = st.slider("Сколько часов ты спал?", min_value=1.0, max_value=15.0, value=8.0, step=0.5)
    quality = st.slider("Качество сна (от 1 до 10)", min_value=1, max_value=10, value=8)
    notes = st.text_input("Заметки (например: лёг поздно, пил кофе, хорошо выспался)")
    
    submitted = st.form_submit_button("💾 Сохранить запись")
    if submitted:
        st.session_state.sleep_data.append({
            "Дата": sleep_date,
            "Часы сна": hours,
            "Качество": quality,
            "Заметки": notes
        })
        st.success("Запись успешно добавлена!")

# Блок аналитики и графиков
if st.session_state.sleep_data:
    st.markdown("---")
    st.subheader("📊 Твоя статистика")
    
    df = pd.DataFrame(st.session_state.sleep_data)
    df["Дата"] = pd.to_datetime(df["Дата"])
    df = df.sort_values("Дата")
    
    # Таблица с историей
    st.dataframe(df, use_container_width=True)
    
    # График динамики сна
    st.markdown("### 📈 Динамика продолжительности сна")
    chart_data = df.set_index("Дата")[["Часы сна"]]
    st.line_chart(chart_data)
    
    # Автоматический анализ последней записи
    last_entry = st.session_state.sleep_data[-1]
    last_hours = last_entry["Часы сна"]
    
    st.markdown("### 💡 Совет по восстановлению:")
    if last_hours < 7:
        st.warning(f"⚠️ Ты спал всего {last_hours} ч. Недостаток сна снижает концентрацию и уровень энергии. Сегодня лучше лечь спать пораньше.")
    elif last_hours > 10:
        st.info(f"💤 Ты проспал {last_hours} ч. Иногда организму нужно отоспаться, но избыток сна тоже может вызывать чувство разбитости.")
    else:
        st.success(f"🟢 Отличный режим ({last_hours} ч)! Оптимальная продолжительность для восстановления сил.")
else:
    st.info("👋 Пока записей нет. Докóжи первую запись через форму выше, чтобы построить графики!")
