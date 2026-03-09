import streamlit as st
import numpy as np

def terrain_analysis(Z,pos):

    st.subheader("地形分析")

    dzdx,dzdy = np.gradient(Z)

    slope = np.sqrt(dzdx**2 + dzdy**2)

    avg_height = np.mean(Z)
    max_height = np.max(Z)

    x = int(pos[0])
    y = int(pos[1])

    st.write("平均高度:",round(avg_height,2))
    st.write("最大高度:",round(max_height,2))
    st.write("当前位置坡度:",round(slope[x][y],3))

    if slope[x][y] > 1.5:
        st.warning("地形坡度较大，飞行风险高")

    else:
        st.success("地形适合飞行")
