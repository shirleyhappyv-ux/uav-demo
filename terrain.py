import numpy as np

def generate_terrain():

    size = 80

    x = np.linspace(-10,10,size)
    y = np.linspace(-10,10,size)

    X,Y = np.meshgrid(x,y)

    Z = (
        5*np.sin(np.sqrt(X**2+Y**2))
        +2*np.cos(Y/2)
        +np.random.rand(size,size)
    )

    return Z
