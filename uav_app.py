import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("无人机飞行与地形分析系统")

# ----------------------
# 操作员登录
# ----------------------

with st.sidebar:

    st.header("操作员登录")

    name = st.text_input("姓名")
    mission = st.text_input("任务编号")

    start = st.button("进入系统")

if not start:
    st.stop()

st.success(f"操作员 {name} 已登录，任务 {mission}")

# ----------------------
# 地形生成
# ----------------------

size = 80

x = np.linspace(-10,10,size)
y = np.linspace(-10,10,size)

X,Y = np.meshgrid(x,y)

Z = (
    6*np.sin(np.sqrt(X**2+Y**2))
    +2*np.cos(X/2)
    +np.random.rand(size,size)
)

# ----------------------
# 无人机控制
# ----------------------

if "drone_pos" not in st.session_state:
    st.session_state.drone_pos = [40,40, Z[40][40]+2]

st.subheader("无人机控制")

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("⬆ 前进"):
        st.session_state.drone_pos[0] +=1

    if st.button("⬅ 左"):
        st.session_state.drone_pos[1] -=1

with col2:
    if st.button("⬇ 后退"):
        st.session_state.drone_pos[0] -=1

with col3:
    if st.button("➡ 右"):
        st.session_state.drone_pos[1] +=1

# 更新高度
x_pos = int(st.session_state.drone_pos[0])
y_pos = int(st.session_state.drone_pos[1])

st.session_state.drone_pos[2] = Z[x_pos][y_pos]+2

# ----------------------
# 地形图
# ----------------------

fig = go.Figure()

fig.add_trace(go.Surface(
    z=Z,
    colorscale="Viridis",
    opacity=0.8
))

fig.add_trace(go.Scatter3d(
    x=[x_pos],
    y=[y_pos],
    z=[st.session_state.drone_pos[2]],
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

# ----------------------
# 地形分析
# ----------------------

st.subheader("地形分析")

dzdx,dzdy = np.gradient(Z)

slope = np.sqrt(dzdx**2 + dzdy**2)

avg_height = np.mean(Z)
max_height = np.max(Z)

st.write("平均高度:",round(avg_height,2))
st.write("最大高度:",round(max_height,2))
st.write("当前位置坡度:",round(slope[x_pos][y_pos],3))

if slope[x_pos][y_pos] > 1.5:
    st.warning("当前区域坡度较大，飞行风险高")
else:
    st.success("地形适合飞行")
