import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Загружаем Excel ===
file_path = "12_sfer_zhizni.xlsx"  # Загрузи файл рядом с этим скриптом
df = pd.read_excel(file_path)

st.title("Колесо Жизни 🌍")
st.markdown("Выставьте значения от 1 до 6 для каждой подсферы, а затем нажмите кнопку для построения колеса.")

# === Сохраняем значения ===
sliders = {}

for sphere in df.columns:
    st.subheader(sphere)
    subs = df[sphere].dropna().tolist()
    sliders[sphere] = []
    for i, sub in enumerate(subs):
        # Создаем уникальный ключ для каждого слайдера
        unique_key = f"{sphere}_{sub}_{i}"
        val = st.slider(
            f"{sub}",
            min_value=1,
            max_value=6,
            value=3,
            step=1,
            key=unique_key  # Добавляем уникальный ключ
        )
        sliders[sphere].append((sub, val))

# === Кнопка для построения колеса ===
if st.button("Создать колесо"):
    # Собираем подсферы и значения
    all_subs = []
    all_values = []
    sphere_colors = {}
    cmap = plt.colormaps.get_cmap("tab20")

    for i, (sphere, subs) in enumerate(sliders.items()):
        subs_names = [s[0] for s in subs]
        vals = [s[1] for s in subs]
        all_subs.extend([(sphere, sub) for sub in subs_names])
        all_values.extend(vals)
        sphere_colors[sphere] = cmap(i / len(df.columns))

    N = len(all_subs)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
    bars = ax.bar(theta, all_values, width=width, align="edge")

    # Раскраска по сферам
    for bar, (sphere, sub) in zip(bars, all_subs):
        bar.set_facecolor(sphere_colors[sphere])
        bar.set_alpha(0.7)

    # Подписи подсфер
    for angle, (sphere, sub), val in zip(theta, all_subs, all_values):
        rotation = np.degrees(angle + width / 2)
        alignment = "left" if np.pi/2 < angle < 3*np.pi/2 else "right"
        ax.text(
            angle + width / 2, 6.5, sub,
            ha=alignment, va="center",
            rotation=rotation, rotation_mode="anchor",
            fontsize=8
        )

    # Настройки осей
    ax.set_ylim(0, 6)
    ax.set_xticks([])
    ax.set_yticks(range(1, 7))
    ax.set_yticklabels(map(str, range(1, 7)))
    ax.set_title("Колесо Жизни", fontsize=18, pad=20)

    # Легенда для сфер
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=sphere_colors[s], alpha=0.7)
        for s in df.columns
    ]
    ax.legend(handles, df.columns, bbox_to_anchor=(1.15, 1.05))

    st.pyplot(fig)