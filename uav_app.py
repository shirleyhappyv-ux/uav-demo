import streamlit as st
import plotly.graph_objects as go
from terrain import generate_terrain
from drone import init_drone, move_drone
from analysis import terrain_analysis

st.set_page_config(layout="wide")

st.title("无人机低空飞行与地形分析 Demo")

# 登录
with st.sidebar:

    st.header("操作员登录")

    name = st.text_input("姓名")
    mission = st.text_input("任务编号")

    start = st.button("进入系统")

if not start:
    st.stop()

st.success(f"操作员 {name} 已进入任务 {mission}")

# 生成地形
Z = generate_terrain()

# 初始化无人机
if "drone" not in st.session_state:
    st.session_state.drone = init_drone(Z)

# 控制区
st.subheader("无人机控制")

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("前进"):
        move_drone("forward",Z)

    if st.button("左"):
        move_drone("left",Z)

with c2:
    if st.button("后退"):
        move_drone("back",Z)

with c3:
    if st.button("右"):
        move_drone("right",Z)

pos = st.session_state.drone

# 3D地形
fig = go.Figure()

fig.add_trace(go.Surface(z=Z,colorscale="Viridis"))

fig.add_trace(go.Scatter3d(
    x=[pos[0]],
    y=[pos[1]],
    z=[pos[2]],
    mode="markers",
    marker=dict(size=6,color="red"),
    name="Drone"
))

st.plotly_chart(fig,use_container_width=True)

# 地形分析
terrain_analysis(Z,pos)
