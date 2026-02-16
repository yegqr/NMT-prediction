import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import numpy as np

st.set_page_config(page_title="НМТ 2024-2025: Повний Аналіз", layout="wide", page_icon="🎯")

# Таблиця переводу балів
SCORE_TABLE = {5: 100, 6: 108, 7: 115, 8: 123, 9: 131, 10: 134, 11: 137, 12: 140, 13: 143,
               14: 145, 15: 147, 16: 148, 17: 149, 18: 150, 19: 151, 20: 152, 21: 155, 22: 159,
               23: 163, 24: 167, 25: 170, 26: 173, 27: 176, 28: 180, 29: 184, 30: 189, 31: 194, 32: 200}

def test_to_nmt_score(test_score):
    if test_score < 5: return 0
    if test_score > 32: return 200
    return SCORE_TABLE.get(int(test_score), 0)

# Стилі
st.markdown("""
<style>
    .main-header {font-size: 3rem; font-weight: bold; text-align: center; 
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;}
    .strategy-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .score-highlight {font-size: 3rem; font-weight: bold; text-align: center; margin: 1rem 0;}
    .insight-box {background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0; 
        border-left: 4px solid #2196f3;}
    .success-box {background: #d4edda; padding: 1rem; border-radius: 8px; margin: 1rem 0; 
        border-left: 4px solid #28a745;}
</style>
""", unsafe_allow_html=True)

# Завантаження даних
try:
    with open('nmt_full_data.json', 'r', encoding='utf-8') as f:
        ALL_DATA = json.load(f)
except FileNotFoundError:
    st.error("❌ Файл nmt_full_data.json не знайдено! Покладіть його в ту ж папку, що й цей скрипт.")
    st.stop()

st.markdown('<p class="main-header">🎯 НМТ 2024-2025: Повна Статистика 1-22</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;">Аналіз 748 відповідей з 34 варіантів НМТ</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Налаштування")
    year_filter = st.radio("🗓️ Рік:", ["📊 Обидва роки", "🔴 НМТ 2024", "🔵 НМТ 2025"], index=0)
    st.markdown("---")
    st.subheader("📈 Розділи:")
    analysis_type = st.radio("", [
        "🎯 КАЛЬКУЛЯТОР БАЛІВ",
        "📊 Статистика по завданнях",
        "💡 Оптимальні стратегії",
        "🔥 Порівняння років"
    ])

# ===== КАЛЬКУЛЯТОР БАЛІВ =====
if analysis_type == "🎯 КАЛЬКУЛЯТОР БАЛІВ":
    st.header("🎯 Калькулятор Балів НМТ з Математики")

    st.markdown("""
    <div class='insight-box'>
        <h3>📚 Структура НМТ з математики (22 завдання = 32 бали)</h3>
        <ul>
            <li><b>Завдання 1-15</b> (по 1 бал) → <b>15 балів</b></li>
            <li><b>Завдання 16-18</b> (по 3 бали за кожен правильний match) → <b>9 балів</b></li>
            <li><b>Завдання 19-22</b> (по 2 бали) → <b>8 балів</b></li>
        </ul>
        <p><b>МАКСИМУМ: 32 тестові бали = 200 балів НМТ</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧮 Розрахуйте свій бал")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📝 Завдання 1-15 (по 1 балу)")
        known_1_15 = st.slider("Скільки знаю напевно:", 0, 15, 10, key="k1")
        strategy_1_15 = st.selectbox("Стратегія для невідомих:", 
            ["Оптимальна (найкраща)", "Завжди А", "Завжди Б", "Завжди В", "Завжди Г", "Завжди Д", "Випадково (1/5)"])

        st.markdown("### 📋 Завдання 16-18 (по 3 бали)")
        st.caption("Кожне завдання має 3 пари → всього 9 балів")
        known_16_18 = st.slider("Скільки балів знаю:", 0, 9, 6, key="k2")

        st.markdown("### 🔢 Завдання 19-22 (по 2 бали)")
        known_19_22 = st.slider("Скільки балів знаю:", 0, 8, 4, key="k3")

    with col2:
        st.markdown("### 📊 Ваш Очікуваний Результат")

        unknown_1_15 = 15 - known_1_15

        # Статистика
        all_answers_1_15 = []
        data_to_use = []
        if year_filter == "🔴 НМТ 2024":
            data_to_use = [ALL_DATA['2024']]
        elif year_filter == "🔵 НМТ 2025":
            data_to_use = [ALL_DATA['2025']]
        else:
            data_to_use = [ALL_DATA['2024'], ALL_DATA['2025']]

        for year_data in data_to_use:
            for date, tasks in year_data.items():
                all_answers_1_15.extend(tasks['1-15'])

        from collections import Counter
        answer_counts = Counter(all_answers_1_15)
        total = len(all_answers_1_15)

        optimal_per_question = []
        for i in range(15):
            q_answers = []
            for year_data in data_to_use:
                for date, tasks in year_data.items():
                    q_answers.append(tasks['1-15'][i])
            optimal_per_question.append(Counter(q_answers).most_common(1)[0][1] / len(q_answers))

        optimal_success = sum(optimal_per_question) / 15

        if "Оптимальна" in strategy_1_15:
            guess_rate = optimal_success
        elif "Випадково" in strategy_1_15:
            guess_rate = 0.2
        else:
            letter = strategy_1_15.split()[-1]
            guess_rate = answer_counts[letter] / total

        guessed_1_15 = unknown_1_15 * guess_rate
        total_test = known_1_15 + guessed_1_15 + known_16_18 + known_19_22
        nmt_score = test_to_nmt_score(total_test)

        st.markdown(f"""
        <div class='strategy-card'>
            <h4 style='text-align: center'>💡 Знаю напевно</h4>
            <p class='score-highlight'>{known_1_15 + known_16_18 + known_19_22:.0f}</p>
            <p style='text-align: center'>балів з 32</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='strategy-card'>
            <h4 style='text-align: center'>🎲 Вгадаю (завд. 1-15)</h4>
            <p class='score-highlight'>{guessed_1_15:.1f}</p>
            <p style='text-align: center'>з {unknown_1_15} невідомих</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='strategy-card'>
            <h4 style='text-align: center'>📝 Тестовий бал</h4>
            <p class='score-highlight'>{total_test:.1f}</p>
            <p style='text-align: center'>з 32 максимум</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='strategy-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'>
            <h4 style='text-align: center'>🏆 БАЛ НМТ</h4>
            <p class='score-highlight'>{nmt_score}</p>
            <p style='text-align: center'>зі шкали 100-200</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Порівняння Всіх Стратегій")

    scenarios = []
    for strat in ["Оптимальна", "Завжди А", "Завжди Б", "Завжди В", "Завжди Г", "Завжди Д", "Випадково"]:
        if strat == "Оптимальна":
            g = unknown_1_15 * optimal_success
        elif strat == "Випадково":
            g = unknown_1_15 * 0.2
        else:
            letter = strat.split()[-1]
            g = unknown_1_15 * (answer_counts[letter] / total)

        ts = known_1_15 + g + known_16_18 + known_19_22
        scenarios.append({
            'Стратегія': strat,
            'Тестовий бал': round(ts, 1),
            'Бал НМТ': test_to_nmt_score(ts)
        })

    scen_df = pd.DataFrame(scenarios).sort_values('Бал НМТ', ascending=False)

    colors_map = {'А': '#FF6B6B', 'Б': '#4ECDC4', 'В': '#45B7D1', 'Г': '#FFA07A', 'Д': '#98D8C8', 
                  'Оптимальна': '#9b59b6', 'Випадково': '#95a5a6'}

    fig = go.Figure()
    for _, row in scen_df.iterrows():
        if 'Завжди' in row['Стратегія']:
            color = colors_map.get(row['Стратегія'].split()[-1], '#95a5a6')
        else:
            color = colors_map.get(row['Стратегія'], '#95a5a6')

        fig.add_trace(go.Bar(
            x=[row['Стратегія']], 
            y=[row['Бал НМТ']],
            marker_color=color,
            text=f"{row['Бал НМТ']}",
            textposition='outside',
            showlegend=False
        ))

    fig.update_layout(
        title=f"Ваш бал НМТ при різних стратегіях вгадування (знаєте {known_1_15}/15)",
        height=500,
        yaxis=dict(range=[0, 210], title="Бал НМТ"),
        xaxis_title="Стратегія"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(scen_df, use_container_width=True, hide_index=True)

    best = scen_df.iloc[0]
    worst = scen_df.iloc[-1]
    diff = best['Бал НМТ'] - worst['Бал НМТ']

    st.markdown(f"""
    <div class='success-box'>
        <h3>🎯 Висновок:</h3>
        <ul>
            <li><b>Найкраща:</b> {best['Стратегія']} → <b>{best['Бал НМТ']} балів НМТ</b></li>
            <li><b>Найгірша:</b> {worst['Стратегія']} → {worst['Бал НМТ']} балів НМТ</li>
            <li><b>Різниця:</b> {diff} балів НМТ! 🚀</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ===== СТАТИСТИКА ПО ЗАВДАННЯХ =====
elif analysis_type == "📊 Статистика по завданнях":
    st.header("📊 Детальна Статистика по Завданнях")

    task_section = st.radio("Оберіть розділ:", ["Завдання 1-15", "Завдання 16-18", "Завдання 19-22"])

    if task_section == "Завдання 1-15":
        st.subheader("📝 Завдання 1-15: Розподіл відповідей А-Д")

        all_answers = []
        data_to_use = []
        if year_filter == "🔴 НМТ 2024":
            data_to_use = [('2024', ALL_DATA['2024'])]
        elif year_filter == "🔵 НМТ 2025":
            data_to_use = [('2025', ALL_DATA['2025'])]
        else:
            data_to_use = [('2024', ALL_DATA['2024']), ('2025', ALL_DATA['2025'])]

        for year, year_data in data_to_use:
            for date, tasks in year_data.items():
                for i, ans in enumerate(tasks['1-15'], 1):
                    all_answers.append({'Рік': year, 'Дата': date, 'Питання': i, 'Відповідь': ans})

        df = pd.DataFrame(all_answers)
        answer_counts = df['Відповідь'].value_counts()

        colors = {'А': '#FF6B6B', 'Б': '#4ECDC4', 'В': '#45B7D1', 'Г': '#FFA07A', 'Д': '#98D8C8'}

        col1, col2, col3, col4, col5 = st.columns(5)
        for col, ans in zip([col1, col2, col3, col4, col5], ['А', 'Б', 'В', 'Г', 'Д']):
            count = answer_counts.get(ans, 0)
            pct = (count / len(df) * 100) if len(df) > 0 else 0
            with col:
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: {colors[ans]}20; 
                     border-radius: 10px; border: 2px solid {colors[ans]}'>
                    <h1 style='color: {colors[ans]}'>{ans}</h1>
                    <h2>{count}</h2>
                    <p style='font-size: 1.2rem; font-weight: bold; color: {colors[ans]}'>{pct:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

        # HEATMAP
        st.markdown("---")
        st.markdown("### 🔥 Heatmap: Частота кожної відповіді для кожного питання")

        heatmap_data = []
        for q in range(1, 16):
            q_answers = df[df['Питання'] == q]['Відповідь']
            row = []
            for ans in ['А', 'Б', 'В', 'Г', 'Д']:
                count = (q_answers == ans).sum()
                row.append(count)
            heatmap_data.append(row)

        heatmap_array = np.array(heatmap_data).T

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_array,
            x=[str(i) for i in range(1, 16)],
            y=['А', 'Б', 'В', 'Г', 'Д'],
            colorscale='RdYlGn',
            text=[[f"{int(val)}" for val in row] for row in heatmap_array],
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Кількість<br>разів")
        ))

        fig_heatmap.update_layout(
            title="Скільки разів кожна відповідь була правильною для кожного питання",
            xaxis=dict(title="Номер питання", side='bottom'),
            yaxis=dict(title="Відповідь"),
            height=400
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
            <h4>💡 Як читати heatmap:</h4>
            <ul>
                <li><b>Зелений колір</b> - ця відповідь часто правильна для цього питання</li>
                <li><b>Жовтий колір</b> - середня частота</li>
                <li><b>Червоний колір</b> - рідко правильна</li>
                <li><b>Число</b> - скільки разів ця відповідь була правильною</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        fig = go.Figure(data=[go.Pie(
            labels=answer_counts.index,
            values=answer_counts.values,
            hole=0.4,
            marker=dict(colors=[colors[a] for a in answer_counts.index])
        )])
        fig.update_layout(title="Загальний розподіл відповідей А-Д", height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 💡 Оптимальна Стратегія для Кожного Питання")

        opt_data = []
        for q in range(1, 16):
            q_answers = df[df['Питання'] == q]['Відповідь']
            most_common = q_answers.value_counts().iloc[0]
            most_common_ans = q_answers.value_counts().index[0]
            total_q = len(q_answers)
            opt_data.append({
                'Питання': q,
                'Обирайте': most_common_ans,
                'Частота': most_common,
                'Успішність': f"{(most_common/total_q*100):.1f}%"
            })

        opt_df = pd.DataFrame(opt_data)
        st.dataframe(opt_df, use_container_width=True, hide_index=True)

    elif task_section == "Завдання 16-18":
        st.subheader("📋 Завдання 16-18: Логічні пари (по 3 бали)")
        st.info("Кожне завдання 16-18 складається з 3 пар відповідностей (А-Д). За кожну правильну пару - 1 бал. Всього 9 балів.")

        task_num = st.selectbox("Оберіть завдання:", [16, 17, 18])

        all_pairs = []
        data_to_use = []
        if year_filter == "🔴 НМТ 2024":
            data_to_use = [('2024', ALL_DATA['2024'])]
        elif year_filter == "🔵 НМТ 2025":
            data_to_use = [('2025', ALL_DATA['2025'])]
        else:
            data_to_use = [('2024', ALL_DATA['2024']), ('2025', ALL_DATA['2025'])]

        for year, year_data in data_to_use:
            for date, tasks in year_data.items():
                answers = tasks[str(task_num)]
                for i, ans in enumerate(answers, 1):
                    all_pairs.append({'Рік': year, 'Дата': date, 'Пара': i, 'Відповідь': ans})

        df_pairs = pd.DataFrame(all_pairs)

        for pair_num in [1, 2, 3]:
            pair_data = df_pairs[df_pairs['Пара'] == pair_num]['Відповідь']
            counts = pair_data.value_counts()

            st.markdown(f"#### Пара {pair_num}")
            cols = st.columns(5)
            for i, (ans, count) in enumerate(counts.items()):
                pct = (count / len(pair_data) * 100) if len(pair_data) > 0 else 0
                cols[i % 5].metric(ans, f"{count}", f"{pct:.1f}%")

    else:
        st.subheader("🔢 Завдання 19-22: Відкрита відповідь (по 2 бали)")
        st.info("Це завдання з відкритою відповіддю (числа). Кожне правильне - 2 бали. Всього 8 балів.")

        task_num = st.selectbox("Оберіть завдання:", [19, 20, 21, 22])

        all_answers = []
        data_to_use = []
        if year_filter == "🔴 НМТ 2024":
            data_to_use = [('2024', ALL_DATA['2024'])]
        elif year_filter == "🔵 НМТ 2025":
            data_to_use = [('2025', ALL_DATA['2025'])]
        else:
            data_to_use = [('2024', ALL_DATA['2024']), ('2025', ALL_DATA['2025'])]

        for year, year_data in data_to_use:
            for date, tasks in year_data.items():
                idx = task_num - 19
                answer = tasks['19-22'][idx]
                all_answers.append({'Рік': year, 'Дата': date, 'Відповідь': answer})

        df_answers = pd.DataFrame(all_answers)

        st.markdown(f"### Всі відповіді на завдання {task_num}:")
        st.dataframe(df_answers, use_container_width=True)

        unique_answers = df_answers['Відповідь'].value_counts()
        st.markdown(f"### Найчастіші відповіді:")
        for ans, count in unique_answers.head(5).items():
            st.write(f"**{ans}** — зустрічається {count} раз(ів)")

# ===== ОПТИМАЛЬНІ СТРАТЕГІЇ (ОНОВЛЕНИЙ РОЗДІЛ) =====
elif analysis_type == "💡 Оптимальні стратегії":
    st.header("💡 Оптимальні Стратегії для Всіх Завдань 1-22")

    st.markdown("""
    <div class='insight-box'>
        <h3>🎯 Як це працює?</h3>
        <p>Аналізуємо реальні правильні відповіді з 34 варіантів НМТ 2024-2025.
        Для кожного завдання показуємо найчастіші правильні відповіді.</p>
    </div>
    """, unsafe_allow_html=True)

    # Вибір даних
    data_to_use = []
    if year_filter == "🔴 НМТ 2024":
        data_to_use = [('2024', ALL_DATA['2024'])]
    elif year_filter == "🔵 НМТ 2025":
        data_to_use = [('2025', ALL_DATA['2025'])]
    else:
        data_to_use = [('2024', ALL_DATA['2024']), ('2025', ALL_DATA['2025'])]

    # ========== ЗАВДАННЯ 1-15 ==========
    st.markdown("---")
    st.subheader("📝 Завдання 1-15: Тести з вибором А-Д")
    st.caption("Кожне завдання: 1 бал | Всього: 15 балів")

    all_answers = []
    for year, year_data in data_to_use:
        for date, tasks in year_data.items():
            for i, ans in enumerate(tasks['1-15'], 1):
                all_answers.append({'Питання': i, 'Відповідь': ans})

    df = pd.DataFrame(all_answers)

    opt_table = []
    for q in range(1, 16):
        q_data = df[df['Питання'] == q]['Відповідь']
        most_common = q_data.value_counts()
        best_ans = most_common.index[0]
        best_count = most_common.iloc[0]
        success_rate = (best_count / len(q_data) * 100)

        alternatives = []
        for i in range(1, min(3, len(most_common))):
            alt_ans = most_common.index[i]
            alt_count = most_common.iloc[i]
            alt_rate = (alt_count / len(q_data) * 100)
            alternatives.append(f"{alt_ans} ({alt_rate:.0f}%)")

        opt_table.append({
            'Питання': q,
            '✅ Краща': best_ans,
            'Успіх': f"{success_rate:.0f}%",
            'Альтернативи': ", ".join(alternatives) if alternatives else "-"
        })

    opt_df = pd.DataFrame(opt_table)
    st.dataframe(opt_df, use_container_width=True, height=600)

    avg_success = sum([float(x['Успіх'].rstrip('%')) for x in opt_table]) / 15
    st.success(f"📊 Середня успішність: **{avg_success:.1f}%** (vs 20% при випадковому виборі)")

    # ========== ЗАВДАННЯ 16-18 ==========
    st.markdown("---")
    st.subheader("📋 Завдання 16-18: Логічні пари")
    st.caption("Кожне завдання: 3 пари × 1 бал = 3 бали | Всього: 9 балів")

    for task_num in [16, 17, 18]:
        st.markdown(f"### Завдання {task_num}")

        all_pairs = []
        for year, year_data in data_to_use:
            for date, tasks in year_data.items():
                answers = tasks[str(task_num)]
                all_pairs.append({
                    'Пара 1': answers[0],
                    'Пара 2': answers[1],
                    'Пара 3': answers[2],
                    'Комбінація': f"{answers[0]}-{answers[1]}-{answers[2]}"
                })

        df_pairs = pd.DataFrame(all_pairs)

        col1, col2, col3 = st.columns(3)

        for i, (col, pair_name) in enumerate([(col1, 'Пара 1'), (col2, 'Пара 2'), (col3, 'Пара 3')], 1):
            pair_data = df_pairs[pair_name].value_counts()
            most_common = pair_data.index[0]
            most_count = pair_data.iloc[0]
            pct = (most_count / len(df_pairs) * 100)

            with col:
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: #e3f2fd; 
                     border-radius: 10px; border: 2px solid #2196f3; margin-bottom: 0.5rem'>
                    <h4>Пара {i}</h4>
                    <h1 style='color: #2196f3; margin: 0.5rem 0'>{most_common}</h1>
                    <p style='font-size: 1.2rem; font-weight: bold; margin: 0'>{pct:.0f}%</p>
                    <p style='font-size: 0.9rem; color: #666; margin: 0'>{most_count}/{len(df_pairs)} разів</p>
                </div>
                """, unsafe_allow_html=True)

                if len(pair_data) > 1:
                    st.caption("Альтернативи:")
                    for j in range(1, min(3, len(pair_data))):
                        alt = pair_data.index[j]
                        alt_count = pair_data.iloc[j]
                        alt_pct = (alt_count / len(df_pairs) * 100)
                        st.caption(f"• {alt}: {alt_pct:.0f}%")

        combo_counts = df_pairs['Комбінація'].value_counts()
        best_combo = combo_counts.index[0]
        best_combo_count = combo_counts.iloc[0]
        best_combo_pct = (best_combo_count / len(df_pairs) * 100)

        st.info(f"💡 **Найчастіша комбінація:** {best_combo} ({best_combo_pct:.0f}% - {best_combo_count}/{len(df_pairs)} разів)")

    # ========== ЗАВДАННЯ 19-22 ==========
    st.markdown("---")
    st.subheader("🔢 Завдання 19-22: Відкрита відповідь (числа)")
    st.caption("Кожне завдання: 2 бали | Всього: 8 балів")

    st.warning("⚠️ **Увага:** Ці завдання НЕ можна вгадати! Потрібні розрахунки. Нижче показано найчастіші відповіді для розуміння типів завдань.")

    for task_num in [19, 20, 21, 22]:
        st.markdown(f"### Завдання {task_num}")

        all_answers_num = []
        for year, year_data in data_to_use:
            for date, tasks in year_data.items():
                idx = task_num - 19
                answer = tasks['19-22'][idx]
                all_answers_num.append({'Рік': year, 'Дата': date, 'Відповідь': answer})

        df_answers = pd.DataFrame(all_answers_num)
        unique_answers = df_answers['Відповідь'].value_counts()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**Топ-5 відповідей:**")
            for i, (ans, count) in enumerate(unique_answers.head(5).items(), 1):
                pct = (count / len(df_answers) * 100)
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
                st.write(f"{emoji} **{ans}** — {count} раз ({pct:.0f}%)")

        with col2:
            if year_filter == "📊 Обидва роки":
                answers_by_year = df_answers.groupby(['Рік', 'Відповідь']).size().reset_index(name='Кількість')
                st.markdown("**Розподіл по роках:**")

                pivot = answers_by_year.pivot(index='Відповідь', columns='Рік', values='Кількість').fillna(0)
                st.dataframe(pivot, use_container_width=True)

    # Загальний висновок
    st.markdown("---")
    st.markdown("""
    <div class='success-box'>
        <h3>🎯 Загальні Рекомендації:</h3>
        <ul>
            <li><b>Завдання 1-15:</b> Використовуйте таблицю вище для невідомих питань</li>
            <li><b>Завдання 16-18:</b> Запам'ятайте найчастіші комбінації для кожного завдання</li>
            <li><b>Завдання 19-22:</b> Ці завдання ПОТРЕБУЮТЬ розрахунків, вгадування не працює!</li>
        </ul>
        <p><b>💡 Стратегія максимізує бали на невідомих питаннях, але НЕ замінює підготовку!</b></p>
    </div>
    """, unsafe_allow_html=True)

# ===== ПОРІВНЯННЯ РОКІВ =====
else:
    st.header("🔥 Порівняння НМТ 2024 vs 2025")

    answers_2024 = []
    for date, tasks in ALL_DATA['2024'].items():
        answers_2024.extend(tasks['1-15'])

    answers_2025 = []
    for date, tasks in ALL_DATA['2025'].items():
        answers_2025.extend(tasks['1-15'])

    from collections import Counter
    counts_2024 = Counter(answers_2024)
    counts_2025 = Counter(answers_2025)

    total_2024 = len(answers_2024)
    total_2025 = len(answers_2025)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### 🔴 НМТ 2024")
        for ans in ['А', 'Б', 'В', 'Г', 'Д']:
            count = counts_2024.get(ans, 0)
            pct = (count / total_2024 * 100) if total_2024 > 0 else 0
            st.metric(ans, count, f"{pct:.1f}%")

    with col2:
        st.markdown("### ⚖️ Різниця")
        for ans in ['А', 'Б', 'В', 'Г', 'Д']:
            diff = counts_2025.get(ans, 0) - counts_2024.get(ans, 0)
            diff_pct = ((counts_2025.get(ans, 0) / total_2025 * 100) if total_2025 > 0 else 0) - \
                       ((counts_2024.get(ans, 0) / total_2024 * 100) if total_2024 > 0 else 0)
            st.metric("Δ", f"{diff:+d}", f"{diff_pct:+.1f}%")

    with col3:
        st.markdown("### 🔵 НМТ 2025")
        for ans in ['А', 'Б', 'В', 'Г', 'Д']:
            count = counts_2025.get(ans, 0)
            pct = (count / total_2025 * 100) if total_2025 > 0 else 0
            st.metric(ans, count, f"{pct:.1f}%")

    fig = go.Figure(data=[
        go.Bar(name='НМТ 2024', x=['А', 'Б', 'В', 'Г', 'Д'],
               y=[counts_2024.get(a, 0) for a in ['А', 'Б', 'В', 'Г', 'Д']],
               marker_color='#ff6b6b'),
        go.Bar(name='НМТ 2025', x=['А', 'Б', 'В', 'Г', 'Д'],
               y=[counts_2025.get(a, 0) for a in ['А', 'Б', 'В', 'Г', 'Д']],
               marker_color='#4ecdc4')
    ])
    fig.update_layout(title="Порівняння розподілів відповідей", barmode='group', height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        <h3>💡 Висновок:</h3>
        <p>Розподіли відповідей у НМТ 2024 та 2025 дуже схожі. 
        Це означає, що стратегії вгадування працюють <b>стабільно</b> для обох років!</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
total_variants = len(ALL_DATA['2024']) + len(ALL_DATA['2025'])
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem'>
    <p>📊 Дашборд на основі {total_variants} варіантів НМТ (748 відповідей на всі завдання)</p>
    <p>🎓 Для освітніх цілей | 💪 Готуйтесь і здавайте на максимум!</p>
</div>
""", unsafe_allow_html=True)
