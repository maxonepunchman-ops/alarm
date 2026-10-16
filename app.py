import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Настройка страницы и темной темы
st.set_page_config(
    page_title="Dark Sleep Matrix",
    page_icon="🧊",
    layout="centered"
)

# Кастомные CSS стили для темного футуристичного интерфейса
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
        margin-top: 10px;
        font-size: 13px;
        color: #8b949e;
    }
    .color-square {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧊 Dark Sleep Matrix & Tracker")
st.markdown("Твой персональный трекер сна с матрицей активности и графиком среднего арифметического.")

# Инициализация данных в сессии (храним по датам количество часов сна и заметку)
if "sleep_matrix" not in st.session_state:
    st.session_state.sleep_matrix = {
        str(date.today() - timedelta(days=2)): {"sleep": 7.0, "note": "Лёг поздно, устал."},
        str(date.today() - timedelta(days=1)): {"sleep": 9.5, "note": "Отлично выспался, максимум энергии."},
        str(date.today()): {"sleep": 8.5, "note": "Хороший режим."}
    }

# --- ФОРМА ВВОДА ДАННЫХ ---
with st.form("sleep_form", clear_on_submit=True):
    st.subheader("✍️ Записать сон за день")
    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("Дата", value=date.today())
    with col2:
        sleep_hours = st.slider("Сколько часов ты спал?", min_value=1.0, max_value=15.0, value=9.0, step=0.5)
    
    note_text = st.text_area("Заметка / самочувствие:", placeholder="Как спалось, были ли мысли, планы...")
    
    submitted = st.form_submit_button("💾 Сохранить в матрицу")
    if submitted:
        st.session_state.sleep_matrix[str(entry_date)] = {
            "sleep": sleep_hours,
            "note": note_text
        }
        st.success(f"Данные за {entry_date} успешно сохранены!")

st.markdown("---")

# --- ФУНКЦИЯ ЦВЕТА КВАДРАТИКА В ЗАВИСИМОСТИ ОТ СОНЯ ---
def get_sleep_color(hours):
    if hours == 0:
        return "#21262d"  # Нет данных (темно-серый)
    elif hours < 6:
        return "#da3633"  # Красный (критический недосып)
    elif 6 <= hours < 7.5:
        return "#9e6a03"  # Желтый / оранжевый (умеренный дефицит)
    elif 7.5 <= hours <= 10:
        return "#238636"  # Зеленый (идеальная норма для подростка)
    else:
        return "#1f6feb"  # Синий (пересып > 10 часов)

# --- МАТРИЦА КВАДРАТИКОВ (АКТИВНОСТЬ ПО ДНЯМ) ---
st.subheader("🔥 Матрица сна (Heatmap)")
st.markdown("Каждый квадратик — один день. Цвет показывает качество сна без лишних цифр.")

days_to_show = 60
end_date = date.today()
start_date = end_date - timedelta(days=days_to_show - 1)
date_list = [start_date + timedelta(days=i) for i in range(days_to_show)]

# Группируем по месяцам для красивых подписей сверху
current_month = ""
cols_per_row = 10
rows = [date_list[i:i + cols_per_row] for i in range(0, len(date_list), cols_per_row)]

for row in rows:
    # Проверяем месяц для заголовка строки
    row_month = row[0].strftime('%B %Y')
    if row_month != current_month:
        current_month = row_month
        st.markdown(f"<p style='color: #8b949e; font-size: 13px; margin-bottom: 5px; margin-top: 15px;'><b>📅 {current_month}</b></p>", unsafe_allow_html=True)
    
    cols = st.columns(len(row))
    for idx, d in enumerate(row):
        d_str = str(d)
        data = st.session_state.sleep_matrix.get(d_str, {"sleep": 0, "note": ""})
        color = get_sleep_color(data["sleep"])
        
        with cols[idx]:
            # Пустой красивый квадратик с закругленными краями (без цифр)
            st.markdown(f"""
                <div style="
                    background-color: {color};
                    border-radius: 6px;
                    height: 38px;
                    border: 1px solid #30363d;
                    margin-bottom: 4px;
                " title="{d_str} | Сон: {data['sleep']}ч"></div>
            """, unsafe_allow_html=True)

# --- ЛЕГЕНДА (ОТДЕЛЬНЫЙ БЛОК СНИЗУ) ---
st.markdown("""
    <div class="custom-card">
        <b>🎨 Легенда цветов матрицы сна:</b>
        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 10px;">
            <div class="legend-box"><div class="color-square" style="background-color: #21262d;"></div> Нет данных</div>
            <div class="legend-box"><div class="color-square" style="background-color: #da3633;"></div> Меньше 6 часов (Критично)</div>
            <div class="legend-box"><div class="color-square" style="background-color: #9e6a03;"></div> 6 - 7.5 часов (Маловато)</div>
            <div class="legend-box"><div class="color-square" style="background-color: #238636;"></div> 7.5 - 10 часов (Идеал для подростка)</div>
            <div class="legend-box"><div class="color-square" style="background-color: #1f6feb;"></div> Больше 10 часов (Пересып)</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- ГРАФИК ПРОГРЕССА ПО СРЕДНЕМУ АРИФМЕТИЧЕСКОМУ ---
st.markdown("---")
st.subheader("📈 График динамики сна (Среднее арифметическое)")
st.markdown("Кривая показывает изменения продолжительности сна. Поднимается при хорошем отдыхе и опускается при недосыпе.")

if st.session_state.sleep_matrix:
    df_list = []
    for d_str, val in st.session_state.sleep_matrix.items():
        df_list.append({"Дата": pd.to_datetime(d_str), "Часы сна": val["sleep"]})
    
    df = pd.DataFrame(df_list).sort_values("Дата")
    
    # Считаем скользящее среднее арифметическое для сглаживания кривой графика
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
    
    # Оценка состояния
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
            <p><b>Всего записей:</b> {total_days} дн.</p>
            <p><b>Средняя продолжительность сна:</b> <code>{avg_sleep:.1f} часа</code> (цель: 9.0 ч.)</p>
            <hr style="border-color: #30363d;">
            <p><b>Экспертная оценка:</b><br>{status_text}</p>
        </div>
    """, unsafe_allow_html=True)

    # Просмотр заметки по конкретному дню
    selected_date = st.selectbox("Выбери дату для просмотра заметки:", options=sorted(list(st.session_state.sleep_matrix.keys()), reverse=True))
    if selected_date:
        day_info = st.session_state.sleep_matrix[selected_date]
        st.info(f"📅 **Дата:** {selected_date} | **Сон:** {day_info['sleep']} ч.\n\n📝 **Заметка:** {day_info['note'] if day_info['note'] else 'Заметка пуста'}")
else:
    st.info("👋 Добавь хотя бы одну запись через форму выше, чтобы построить матрицу, график и сводку!")
