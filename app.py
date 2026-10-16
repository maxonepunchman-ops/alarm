import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# Настройка страницы и темной темы
st.set_page_config(
    page_title="Dark Sleep Matrix",
    page_icon="🧊",
    layout="centered"
)

# Кастомные CSS стили для сетки с днями недели и месяцами
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
    /* Сетка хитмапа */
    .heatmap-wrapper {
        display: flex;
        gap: 8px;
        align-items: flex-start;
        overflow-x: auto;
        padding-bottom: 10px;
    }
    .days-labels {
        display: flex;
        flex-direction: column;
        gap: 5px;
        font-size: 11px;
        color: #8b949e;
        padding-top: 2px;
        text-align: right;
        min-width: 20px;
    }
    .day-label {
        height: 24px;
        line-height: 24px;
    }
    .heatmap-grid {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .heat-row {
        display: flex;
        gap: 5px;
    }
    .heat-box {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        border: 1px solid #30363d;
    }
    /* Читаемые шрифты для полей */
    label, .stTimeInput label, .stTextArea label {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #e6edf3 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧊 Dark Sleep Matrix")
st.markdown("Твой персональный трекер сна: авторасчет времени, календарная сетка и аналитика.")

# Инициализация данных в сессии (храним только реальные дни)
today_str = str(date.today())
yesterday_str = str(date.today() - timedelta(days=1))

if "sleep_matrix" not in st.session_state:
    st.session_state.sleep_matrix = {
        yesterday_str: {"sleep": 8.5, "bedtime": "23:00", "waketime": "07:30", "note": "Хороший режим."},
        today_str: {"sleep": 9.0, "bedtime": "22:30", "waketime": "07:30", "note": "Идеально выспался."}
    }

# --- ФОРМА ВВОДА (АВТОМАТИЧЕСКАЯ ДАТА + РАСЧЕТ ВРЕМЕНИ) ---
with st.form("sleep_form", clear_on_submit=True):
    st.subheader(f"✍️ Сон за сегодня ({date.today().strftime('%d.%m.%Y')})")
    
    col1, col2 = st.columns(2)
    with col1:
        bed_time = st.time_input("🌙 Во сколько лег?", value=datetime.strptime("23:00", "%H:%M").time())
    with col2:
        wake_time = st.time_input("☀️ Во сколько встал?", value=datetime.strptime("07:30", "%H:%M").time())
    
    note_text = st.text_area("📝 Заметка / самочувствие:", placeholder="Как спалось, мысли...")
    
    submitted = st.form_submit_button("💾 Сохранить в матрицу", use_container_width=True)
    
    if submitted:
        # Автоматический расчет часов сна
        dt_bed = datetime.combine(date.today(), bed_time)
        dt_wake = datetime.combine(date.today(), wake_time)
        
        # Если легли вечером, а встали утром (переход через полночь)
        if dt_wake <= dt_bed:
            dt_wake += timedelta(days=1)
        
        sleep_duration = round((dt_wake - dt_bed).total_seconds() / 3600, 1)
        
        # Сохраняем на сегодняшнюю дату
        st.session_state.sleep_matrix[today_str] = {
            "sleep": sleep_duration,
            "bedtime": bed_time.strftime("%H:%M"),
            "waketime": wake_time.strftime("%H:%M"),
            "note": note_text
        }
        st.success(f"Готово! Засчитано сна: {sleep_duration} ч.")

st.markdown("---")

# --- ФУНКЦИЯ ЦВЕТА ---
def get_sleep_color(hours):
    if hours == 0:
        return "#161b22"  # Пустой день без записи
    elif hours < 6:
        return "#da3633"  # Красный (критический недосып)
    elif 6 <= hours < 7.5:
        return "#9e6a03"  # Оранжевый (маловато)
    elif 7.5 <= hours <= 10:
        return "#238636"  # Зеленый (идеал для подростка)
    else:
        return "#1f6feb"  # Синий (пересып)

# --- МАТРИЦА С ДНЯМИ НЕДЕЛИ И МЕСЯЦАМИ ---
st.subheader("🔥 Матрица сна (Heatmap)")
st.markdown("Календарная сетка за последние недели. Дни недели слева, месяцы сверху.")

# Генерация дней (последние 4 недели для красивой матрицы по дням недели)
days_to_show = 28  
end_date = date.today()
start_date = end_date - timedelta(days=days_to_show - 1)

# Выравниваем по понедельникам
start_date = start_date - timedelta(days=start_date.weekday())
all_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# Дни недели (Пн, Вт, Ср, Чт, Пт, Сб, Вс)
weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

# Группируем по неделям (колонкам)
weeks = []
current_week = []
for d in all_days:
    current_week.append(d)
    if d.weekday() == 6 or d == end_date:
        weeks.append(current_week)
        current_week = []

# Отрисовка матрицы с подписями дней недели слева
heatmap_html = '<div class="heatmap-wrapper">'
heatmap_html += '<div class="days-labels">'
for day_name in weekdays:
    heatmap_html += f'<div class="day-label">{day_name}</div>'
heatmap_html += '</div>'

heatmap_html += '<div style="display: flex; gap: 5px;">'
for week in weeks:
    heatmap_html += '<div class="heatmap-grid">'
    # Заполняем пустые дни, если неделя началась не с понедельника
    for _ in range(7 - len(week)):
        # пустой слот для выравнивания
        pass
    
    for d in week:
        d_str = str(d)
        data = st.session_state.sleep_matrix.get(d_str, {"sleep": 0})
        color = get_sleep_color(data["sleep"])
        heatmap_html += f'<div class="heat-box" style="background-color: {color};" title="{d_str} | Сон: {data["sleep"]}ч"></div>'
    heatmap_html += '</div>'
heatmap_html += '</div></div>'

st.markdown(heatmap_html, unsafe_allow_html=True)

# --- ЛЕГЕНДА ОТДЕЛЬНЫМ БЛОКОМ СНИЗУ ---
st.markdown("""
    <div class="custom-card" style="margin-top: 15px;">
        <b>🎨 Легенда цветов матрицы сна:</b>
        <div class="legend-box"><div class="color-square" style="background-color: #161b22;"></div> Нет данных / Будущее</div>
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
        if val["sleep"] > 0:
            df_list.append({"Дата": pd.to_datetime(d_str), "Часы сна": val["sleep"]})
    
    if df_list:
        df = pd.DataFrame(df_list).sort_values("Дата")
        df["Среднее (арифм.)"] = df["Часы сна"].expanding().mean()
        df["Идеальная норма"] = 9.0
        
        chart_df = df.set_index("Дата")[["Часы сна", "Среднее (арифм.)", "Идеальная норма"]]
        st.line_chart(chart_df)

# --- СВОДКА И АНАЛИТИКА СНИЗУ ---
st.markdown("---")
st.subheader("📋 Сводка и анализ твоего сна")

valid_entries = [v for v in st.session_state.sleep_matrix.values() if v["sleep"] > 0]
if valid_entries:
    total_days = len(valid_entries)
    avg_sleep = sum([v["sleep"] for v in valid_entries]) / total_days
    
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
else:
    st.info("👋 Добавь запись за сегодня через форму выше!")
