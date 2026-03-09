import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="无人机航线规划仿真系统", layout="wide")

st.title("低空无人机航线规划仿真系统 Demo")

# -------------------------
# 初始化状态
# -------------------------

if "lat" not in st.session_state:
    st.session_state.lat = 39.90

if "lon" not in st.session_state:
    st.session_state.lon = 116.40

if "path" not in st.session_state:
    st.session_state.path = [(st.session_state.lat, st.session_state.lon)]

if "terrain_result" not in st.session_state:
    st.session_state.terrain_result = "平原：适合低空飞行"

# -------------------------
# 地形分析函数
# -------------------------

def terrain_analysis(lat, lon):

    v = int((lat * 100 + lon * 100)) % 4

    if v == 0:
        return "平原：适合低空飞行"

    elif v == 1:
        return "丘陵：建议保持80m以上高度"

    elif v == 2:
        return "山地：建议绕行或升高飞行"

    else:
        return "河谷：可沿河谷低空巡航"

# -------------------------
# 无人机移动函数
# -------------------------

def move(dx, dy):

    st.session_state.lat += dx
    st.session_state.lon += dy

    new_pos = (st.session_state.lat, st.session_state.lon)

    st.session_state.path.append(new_pos)

    st.session_state.terrain_result = terrain_analysis(
        st.session_state.lat,
        st.session_state.lon
    )

# -------------------------
# 控制按钮
# -------------------------

st.subheader("无人机控制")

col1, col2, col3 = st.columns(3)

with col2:
    st.button("⬆ 前进", on_click=move, args=(0.01, 0))

col4, col5, col6 = st.columns(3)

with col4:
    st.button("⬅ 左移", on_click=move, args=(0, -0.01))

with col5:
    st.button("⬇ 后退", on_click=move, args=(-0.01, 0))

with col6:
    st.button("➡ 右移", on_click=move, args=(0, 0.01))

# -------------------------
# 显示无人机坐标
# -------------------------

st.write(
    "当前无人机坐标：",
    round(st.session_state.lat, 4),
    round(st.session_state.lon, 4)
)

# -------------------------
# 地图绘制
# -------------------------

m = folium.Map(
    location=[st.session_state.lat, st.session_state.lon],
    zoom_start=12
)

# 无人机位置

folium.Marker(
    [st.session_state.lat, st.session_state.lon],
    tooltip="无人机",
    icon=folium.Icon(color="red", icon="plane")
).add_to(m)

# 飞行轨迹

folium.PolyLine(
    st.session_state.path,
    color="blue",
    weight=3
).add_to(m)

st.subheader("飞行地图")

st_folium(
    m,
    width=900,
    height=500
)

# -------------------------
# 地形分析结果
# -------------------------

st.subheader("地形分析结果")

st.write(st.session_state.terrain_result)

# -------------------------
# 飞行任务总结
# -------------------------

st.subheader("飞行任务统计")

st.write("飞行步数：", len(st.session_state.path))

st.write("当前飞行区域分析：")

if "山地" in st.session_state.terrain_result:

    st.warning("⚠ 当前区域为山地，建议提高飞行高度")

elif "丘陵" in st.session_state.terrain_result:

    st.info("注意坡度变化，建议保持稳定高度")

elif "河谷" in st.session_state.terrain_result:

    st.success("河谷区域适合巡航")

else:

    st.success("当前区域适合低空飞行")

# -------------------------
# 重置按钮
# -------------------------

if st.button("重置飞行任务"):

    st.session_state.lat = 39.90
    st.session_state.lon = 116.40
    st.session_state.path = [(39.90,116.40)]
    st.session_state.terrain_result = "平原：适合低空飞行"

    st.rerun()
