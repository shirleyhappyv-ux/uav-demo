import streamlit as st
import numpy as np

def terrain_analysis(Z,pos):

    x,y,z = pos

    h = Z[int(x)][int(y)]

    slope = np.gradient(Z)[0][int(x)][int(y)]

    st.subheader("地形分析报告")

    st.write("地面高度:",round(h,2))

    st.write("无人机高度:",round(z,2))

    st.write("坡度:",round(abs(slope),2))

    if h > 70:

        st.warning("山地区域，建议提升高度")

    elif abs(slope) > 3:

        st.info("丘陵区域，注意地形变化")

    else:

        st.success("平原区域，适合低空飞行")
