import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Настройка страницы и темной темы
st.set_page_config(
    page_title="Dark Notes & Sleep Tracker",
    page_icon="🧊",
    layout="centered"
)

# Кастомные стили CSS для темной темы и закругленных карточек
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧊 Dark Habit & Sleep Matrix")
st.markdown("Твой личный трекер: темный футуристичный интерфейс, матрица активности и график прогресса сна.")

# Инициализация базы данных в сессии
if "matrix_data" not in st.session_state:
    st.session_state.matrix_data = {
        str(date.today() - timedelta(days=2)): {"sleep": 8.0, "score": 3, "note": "Лег вовремя, продуктивный день."},
        str(date.today() - timedelta(days=1)): {"sleep": 9.5, "score": 5, "note": "Идеально выспался, максимум энергии."},
        str(date.today()): {"sleep": 7.0, "score": 2, "note": "Засиделся за кодом, надо наверстать."}
    }

# --- ФОРМА ДОБАВЛЕНИЯ ЗАПИСИ ---
with st.form("entry_form", clear_on_submit=True):
    st.subheader("✍️ Добавить запись за день")
    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("Дата", value=date.today())
    with col2:
        sleep_hours = st.slider("Сколько часов спал?", min_value=1.0, max_value=15.0, value=9.0, step=0.5)
    
    score = st.slider("Уровень активности / продуктивности (0 - 5)", min_value=0, max_value=5, value=3)
    note_text = st.text_area("Заметка (мысли, итоги, планы):", placeholder="Потренировался, пописал код...")
    
    submitted = st.form_submit_button("💾 Сохранить в систему")
    if submitted:
        st.session_state.matrix_data[str(entry_date)] = {
            "sleep": sleep_hours,
            "score": score,
            "note": note_text
        }
        st.success(f"Запись за {entry_date} успешно сохранена!")

st.markdown("---")
st.subheader("🔥 Матрица активности (Heatmap)")
st.markdown("Каждый квадратик — день. Цвет зависит от уровня активности. Ниже можно посмотреть детали по любому дню.")

# --- ГЕНЕРАЦИЯ СЕТКИ КВАДРАТИКОВ ЗА ПОСЛЕДНИЕ 60 ДНЕЙ ---
days_to_show = 60
end_date = date.today()
start_date = end_date - timedelta(days=days_to_show - 1)
date_list = [start_date + timedelta(days=i) for i in range(days_to_show)]

def get_color(score):
    colors = {
        0: "#21262d",  
        1: "#0e4429",  
        2: "#006d32",  
        3: "#26a641",  
        4: "#39d353",  
        5: "#56d364"   
    }
    return colors.get(score, "#21262d")

cols_per_row = 10
rows = [date_list[i:i + cols_per_row] for i in range(0, len(date_list), cols_per_row)]

for row in rows:
    cols = st.columns(len(row))
    for idx, d in enumerate(row):
        d_str = str(d)
        data = st.session_state.matrix_data.get(d_str, {"sleep": 0, "score": 0, "note": "Нет записей"})
        color = get_color(data["score"])
        
        with cols[idx]:
            st.markdown(f"""
                <div style="
                    background-color: {color};
                    border-radius: 8px;
                    height: 45px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 11px;
                    font-weight: bold;
                    border: 1px solid #30363d;
                    margin-bottom: 5px;
                " title="{d_str} | Сон: {data['sleep']}ч | Активность: {data['score']}">
                    {d.strftime('%d.%m')}
                </div>
            """, unsafe_allow_html=True)

# --- ГРАФИК ПРОГРЕССА СНА ---
st.markdown("---")
st.subheader("📈 График прогресса: Продолжительность сна")
st.markdown("Сравнение твоего сна с идеальной нормой для подростка (**9 часов**).")

if st.session_state.matrix_data:
    # Превращаем данные в DataFrame для графиков
    df_list = []
    for d_str, val in st.session_state.matrix_data.items():
        df_list.append({"Дата": d_str, "Часы сна": val["sleep"], "Идеал": 9.0})
    
    df = pd.DataFrame(df_list)
    df["Дата"] = pd.to_datetime(df["Дата"])
    df = df.sort_values("Дата")
    df = df.set_index("Дата")
    
    # Выводим красивый линейный график (показывает часы сна и линию идеала)
    st.line_chart(df[["Часы сна", "Идеал"]])

st.markdown("---")
st.subheader("🔍 Просмотр информации по конкретному дню")

selected_date = st.selectbox("Выбери дату:", options=sorted(list(st.session_state.matrix_data.keys()), reverse=True))

if selected_date:
    day_info = st.session_state.matrix_data[selected_date]
    st.markdown(f"""
        <div class="metric-card">
            <h3>📅 Дата: {selected_date}</h3>
            <p><b>😴 Продолжительность сна:</b> {day_info['sleep']} ч. (Норма: 9 ч.)</p>
            <p><b>⚡ Уровень активности:</b> {day_info['score']} / 5</p>
            <p><b>📝 Заметка:</b><br>{day_info['note'] if day_info['note'] else '<i>Заметка пуста</i>'}</p>
        </div>
    """, unsafe_allow_html=True)
