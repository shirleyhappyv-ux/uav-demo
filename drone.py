import streamlit as st

def init_drone(Z):

    x = 40
    y = 40
    z = Z[x][y] + 2

    return [x,y,z]


def move_drone(direction,Z):

    drone = st.session_state.drone

    if direction == "forward":
        drone[0] +=1

    if direction == "back":
        drone[0] -=1

    if direction == "left":
        drone[1] -=1

    if direction == "right":
        drone[1] +=1

    x = int(drone[0])
    y = int(drone[1])

    drone[2] = Z[x][y] + 2

    st.session_state.drone = drone
