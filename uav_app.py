import streamlit as st
import plotly.graph_objects as go

from terrain import generate_terrain
from drone import init_drone,move_drone
from planner import astar
from analysis import terrain_analysis

st.set_page_config(layout="wide")

st.title("无人机侦察与地形分析系统")

# ----------------
# Session状态
# ----------------

if "login" not in st.session_state:
    st.session_state.login = False

if "terrain" not in st.session_state:
    st.session_state.terrain = None

if "path" not in st.session_state:
    st.session_state.path = []

# ----------------
# 登录
# ----------------

with st.sidebar:

    st.header("操作员登录")

    name = st.text_input("姓名")

    mission = st.text_input("任务")

    if st.button("进入系统"):

        st.session_state.login = True

        st.session_state.name = name

        st.session_state.mission = mission

if not st.session_state.login:

    st.info("请输入操作员信息")

    st.stop()

st.success(f"操作员 {st.session_state.name} 执行任务 {st.session_state.mission}")

# ----------------
# 地形生成
# ----------------

if st.session_state.terrain is None:

    st.session_state.terrain = generate_terrain()

Z = st.session_state.terrain

# ----------------
# 无人机初始化
# ----------------

if "drone" not in st.session_state:

    st.session_state.drone = init_drone(Z)

pos = st.session_state.drone

# ----------------
# 控制区
# ----------------

st.subheader("无人机控制")

c1,c2,c3,c4 = st.columns(4)

with c1:
    if st.button("前进"):
        st.session_state.drone = move_drone("forward",Z)

with c2:
    if st.button("后退"):
        st.session_state.drone = move_drone("back",Z)

with c3:
    if st.button("左"):
        st.session_state.drone = move_drone("left",Z)

with c4:
    if st.button("右"):
        st.session_state.drone = move_drone("right",Z)

pos = st.session_state.drone

st.session_state.path.append(pos)

# ----------------
# 自动航线规划
# ----------------

st.subheader("自动航线规划")

goal_x = st.slider("目标X",0,Z.shape[0]-1,40)

goal_y = st.slider("目标Y",0,Z.shape[1]-1,40)

if st.button("自动规划"):

    start = (int(pos[0]),int(pos[1]))

    goal = (goal_x,goal_y)

    route = astar(Z,start,goal)

    st.session_state.path = []

    for r in route:

        st.session_state.path.append([r[0],r[1],Z[r[0]][r[1]]+20])

# ----------------
# 3D显示
# ----------------

fig = go.Figure()

fig.add_trace(go.Surface(z=Z,colorscale="Viridis",opacity=0.8))

fig.add_trace(go.Scatter3d(

    x=[p[0] for p in st.session_state.path],

    y=[p[1] for p in st.session_state.path],

    z=[p[2] for p in st.session_state.path],

    mode="lines",

    line=dict(width=6,color="red"),

    name="Flight Path"

))

fig.add_trace(go.Scatter3d(

    x=[pos[0]],

    y=[pos[1]],

    z=[pos[2]],

    mode="markers",

    marker=dict(size=8,color="yellow"),

    name="Drone"

))

fig.update_layout(

    scene=dict(

        xaxis_title="X",

        yaxis_title="Y",

        zaxis_title="Height"

    )

)

st.plotly_chart(fig,use_container_width=True)

# ----------------
# 地形分析
# ----------------

terrain_analysis(Z,pos)
