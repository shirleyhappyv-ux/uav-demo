import streamlit as st
import numpy as np
import plotly.graph_objects as go
from terrain import generate_terrain
from drone import init_drone, move_drone
from analysis import terrain_analysis

st.set_page_config(layout="wide")

st.title("无人机低空飞行与地形分析 Demo")

# ------------------------
# Session 状态初始化
# ------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "terrain" not in st.session_state:
    st.session_state.terrain = None

# ------------------------
# 登录界面
# ------------------------

with st.sidebar:

    st.header("操作员登录")

    name = st.text_input("姓名")
    mission = st.text_input("任务编号")

    if st.button("进入系统"):
        st.session_state.logged_in = True
        st.session_state.name = name
        st.session_state.mission = mission

# 未登录
if not st.session_state.logged_in:
    st.info("请输入操作员信息并点击进入系统")
    st.stop()

st.success(f"操作员 {st.session_state.name} 已进入任务 {st.session_state.mission}")

# ------------------------
# 地形生成（只生成一次）
# ------------------------

if st.session_state.terrain is None:
    st.session_state.terrain = generate_terrain()

Z = st.session_state.terrain

# ------------------------
# 初始化无人机
# ------------------------

if "drone" not in st.session_state:
    st.session_state.drone = init_drone(Z)

# ------------------------
# 控制区
# ------------------------

st.subheader("无人机控制")

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("⬆ 前进"):
        move_drone("forward",Z)

    if st.button("⬅ 左"):
        move_drone("left",Z)

with c2:
    if st.button("⬇ 后退"):
        move_drone("back",Z)

with c3:
    if st.button("➡ 右"):
        move_drone("right",Z)

pos = st.session_state.drone

# ------------------------
# 3D地形显示
# ------------------------

fig = go.Figure()

fig.add_trace(go.Surface(
    z=Z,
    colorscale="Viridis",
    opacity=0.8
))

fig.add_trace(go.Scatter3d(
    x=[pos[0]],
    y=[pos[1]],
    z=[pos[2]],
    mode="markers",
    marker=dict(size=6,color="red"),
    name="Drone"
))

fig.update_layout(
    title="无人机飞行仿真",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Height"
    )
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------
# 地形分析
# ------------------------

terrain_analysis(Z,pos)
