import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="无人机航线规划仿真", layout="wide")

st.title("低空无人机航线规划仿真系统")

# 初始化状态
if "x" not in st.session_state:
    st.session_state.x = 39.90
    st.session_state.y = 116.40

if "terrain" not in st.session_state:
    st.session_state.terrain = "平原"

# 模拟地形分析
def terrain_analysis():
    terrains = ["平原", "丘陵", "山地", "河谷"]
    st.session_state.terrain = random.choice(terrains)

# 无人机移动
def move(dx, dy):
    st.session_state.x += dx
    st.session_state.y += dy
    terrain_analysis()

# 控制按钮
col1, col2, col3 = st.columns(3)

with col1:
    st.button("⬅ 后退", on_click=move, args=(0, -0.01))

with col2:
    st.button("⬆ 前进", on_click=move, args=(0.01, 0))

with col3:
    st.button("➡ 右移", on_click=move, args=(0, 0.01))

# 绘制地图
m = folium.Map(location=[st.session_state.x, st.session_state.y], zoom_start=12)

folium.Marker(
    [st.session_state.x, st.session_state.y],
    tooltip="无人机位置",
    icon=folium.Icon(color="red", icon="plane")
).add_to(m)

st_folium(m, width=700, height=500)

# 地形分析
st.subheader("地形分析结果")

st.write("当前位置地形：", st.session_state.terrain)

if st.session_state.terrain == "山地":
    st.warning("⚠ 建议提高飞行高度")

elif st.session_state.terrain == "河谷":
    st.info("建议沿河谷飞行")

elif st.session_state.terrain == "丘陵":
    st.info("注意坡度变化")

else:
    st.success("适合低空飞行")
