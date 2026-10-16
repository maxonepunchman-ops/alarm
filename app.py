import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Настройка страницы и темной темы
st.set_page_config(
    page_title="Dark Sleep Matrix",
    page_icon="🧊",
    layout="centered"
)

# Кастомные CSS стили: жесткая сетка квадратиков, крупный шрифт и чистые формы
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .custom-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .legend-box {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 8px;
        font-size: 13px;
        color: #8b949e;
    }
    .color-square {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        border: 1px solid #30363d;
    }
    /* Сетка квадратиков как на GitHub */
    .heatmap-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 15px;
    }
    .heat-box {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        border: 1px solid #30363d;
    }
    /* Увеличенный и читаемый текст для полей ввода */
    label, .stTextInput label, .stSlider label, .stDateInput label {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #e6edf3 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧊 Dark Sleep Matrix & Tracker")
st.markdown("Твой персональный трекер сна: аккуратная сетка, график и удобный ввод.")

# Инициализация данных в сессии
if "sleep_matrix" not in st.session_state:
    st.session_state.sleep_matrix = {
        str(date.today() - timedelta(days=2)): {"sleep": 7.0, "note": "Лёг поздно, устал."},
        str(date.today() - timedelta(days=1)): {"sleep": 9.5, "note": "Отлично выспался, максимум энергии."},
        str(date.today()): {"sleep": 8.5, "note": "Хороший режим."}
    }

# --- НОРМАЛЬНАЯ, ЧИТАЕМАЯ ФОРМА ВВОДА ---
with st.form("sleep_form", clear_on_submit=True):
    st.subheader("✍️ Добавить запись за день")
    
    entry_date = st.date_input("📅 Выбери дату:", value=date.today())
    
    st.markdown("<br>", unsafe_allow_html=True)
    sleep_hours = st.slider("😴 Сколько часов ты спал?", min_value=1.0, max_value=15.0, value=9.0, step=0.5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    note_text = st.text_area("📝 Заметка / самочувствие:", placeholder="Как спалось, мысли, планы...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("💾 Сохранить в матрицу", use_container_width=True)
    
    if submitted:
        st.session_state.sleep_matrix[str(entry_date)] = {
            "sleep": sleep_hours,
            "note": note_text
        }
        st.success(f"Данные за {entry_date} успешно сохранены!")

st.markdown("---")

# --- ФУНКЦИЯ ЦВЕТА ---
def get_sleep_color(hours):
    if hours == 0:
        return "#21262d"  # Нет данных
    elif hours < 6:
        return "#da3633"  # Красный (критический недосып)
    elif 6 <= hours < 7.5:
        return "#9e6a03"  # Оранжевый (маловато)
    elif 7.5 <= hours <= 10:
        return "#238636"  # Зеленый (идеал для подростка)
    else:
        return "#1f6feb"  # Синий (пересып)

# --- ИДЕАЛЬНАЯ СЕТКА КВАДРАТИКОВ (HEATMAP) ---
st.subheader("🔥 Матрица сна (Heatmap)")
st.markdown("Каждый квадратик — один день. Цвет показывает качество сна.")

days_to_show = 60
end_date = date.today()
start_date = end_date - timedelta(days=days_to_show - 1)
date_list = [start_date + timedelta(days=i) for i in range(days_to_show)]

# Рендерим квадратики через компактный flex-контейнер, чтобы они идеально вмещались на экране телефона
boxes_html = '<div class="heatmap-grid">'
for d in date_list:
    d_str = str(d)
    data = st.session_state.sleep_matrix.get(d_str, {"sleep": 0})
    color = get_sleep_color(data["sleep"])
    boxes_html += f'<div class="heat-box" style="background-color: {color};" title="{d_str} | Сон: {data["sleep"]}ч"></div>'
boxes_html += '</div>'

st.markdown(boxes_html, unsafe_allow_html=True)

# --- ЛЕГЕНДА ОТДЕЛЬНЫМ БЛОКОМ СНИЗУ ---
st.markdown("""
    <div class="custom-card">
        <b>🎨 Легенда цветов матрицы сна:</b>
        <div class="legend-box"><div class="color-square" style="background-color: #21262d;"></div> Нет данных</div>
        <div class="legend-box"><div class="color-square" style="background-color: #da3633;"></div> Меньше 6 часов (Критично)</div>
        <div class="legend-box"><div class="color-square" style="background-color: #9e6a03;"></div> 6 - 7.5 часов (Маловато)</div>
        <div class="legend-box"><div class="color-square" style="background-color: #238636;"></div> 7.5 - 10 часов (Идеал для подростка)</div>
        <div class="legend-box"><div class="color-square" style="background-color: #1f6feb;"></div> Больше 10 часов (Пересып)</div>
    </div>
""", unsafe_allow_html=True)

# --- ГРАФИК ПРОГРЕССА (СРЕДНЕЕ АРИФМЕТИЧЕСКОЕ) ---
st.markdown("---")
st.subheader("📈 График динамики сна (Среднее арифметическое)")
st.markdown("Кривая показывает изменения продолжительности сна. Поднимается при хорошем отдыхе и опускается при недосыпе.")

if st.session_state.sleep_matrix:
    df_list = []
    for d_str, val in st.session_state.sleep_matrix.items():
        df_list.append({"Дата": pd.to_datetime(d_str), "Часы сна": val["sleep"]})
    
    df = pd.DataFrame(df_list).sort_values("Дата")
    df["Среднее (арифм.)"] = df["Часы сна"].expanding().mean()
    df["Идеальная норма"] = 9.0
    
    chart_df = df.set_index("Дата")[["Часы сна", "Среднее (арифм.)", "Идеальная норма"]]
    st.line_chart(chart_df)

# --- СВОДКА И АНАЛИТИКА СНИЗУ ---
st.markdown("---")
st.subheader("📋 Сводка и анализ твоего сна")

if st.session_state.sleep_matrix:
    total_days = len(st.session_state.sleep_matrix)
    avg_sleep = sum([v["sleep"] for v in st.session_state.sleep_matrix.values()]) / total_days
    
    if avg_sleep >= 8.5:
        status_text = "🟢 Отличный режим! Ты держишься близко к идеальной подростковой норме в 9 часов. Мозг и тело восстанавливаются на максимум."
        status_color = "#238636"
    elif avg_sleep >= 7.0:
        status_text = "🟡 Нормальный уровень, но есть небольшой дефицит. Постарайся ложиться на 30–40 минут раньше, чтобы выйти на стабильные 9 часов."
        status_color = "#9e6a03"
    else:
        status_text = "🔴 Хронический недосып! Организм работает на износ. Срочно нужно выстроить режим и ложиться спать вовремя."
        status_color = "#da3633"

    st.markdown(f"""
        <div class="custom-card">
            <h4 style="margin-top: 0; color: {status_color};">📊 Итоги за весь период:</h4>
            <p style="font-size: 15px;"><b>Всего записей:</b> {total_days} дн.</p>
            <p style="font-size: 15px;"><b>Средняя продолжительность сна:</b> <code>{avg_sleep:.1f} часа</code> (цель: 9.0 ч.)</p>
            <hr style="border-color: #30363d;">
            <p style="font-size: 15px;"><b>Экспертная оценка:</b><br>{status_text}</p>
        </div>
    """, unsafe_allow_html=True)

    selected_date = st.selectbox("📅 Выбери дату для просмотра заметки:", options=sorted(list(st.session_state.sleep_matrix.keys()), reverse=True))
    if selected_date:
        day_info = st.session_state.sleep_matrix[selected_date]
        st.info(f"📅 **Дата:** {selected_date} | **Сон:** {day_info['sleep']} ч.\n\n📝 **Заметка:** {day_info['note'] if day_info['note'] else 'Заметка пуста'}")
else:
    st.info("👋 Добавь хотя бы одну запись через форму выше!")
