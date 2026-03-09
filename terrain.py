import numpy as np

def generate_terrain(size=60):

    x = np.linspace(-5,5,size)
    y = np.linspace(-5,5,size)

    X,Y = np.meshgrid(x,y)

    Z = (
        np.sin(X)*np.cos(Y)*30
        + np.random.randn(size,size)*2
        + 50
    )

    return Z
