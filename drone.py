import streamlit as st

def init_drone(Z):

    x = Z.shape[0]//2
    y = Z.shape[1]//2
    z = Z[x][y] + 20

    return [x,y,z]

def move_drone(direction,Z):

    x,y,z = st.session_state.drone

    if direction == "forward":
        x = min(x+1,Z.shape[0]-1)

    if direction == "back":
        x = max(x-1,0)

    if direction == "left":
        y = max(y-1,0)

    if direction == "right":
        y = min(y+1,Z.shape[1]-1)

    z = Z[x][y] + 20

    return [x,y,z]
