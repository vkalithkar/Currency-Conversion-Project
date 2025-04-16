import numpy as np

TAU = 2*np.pi

def get_data(n: int = 100, 
             freq: float = 1
             ) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(0, 10, n)
    y = np.sin(TAU*x*freq)
    return x, y

def sigmoid(a: float = 1, 
            k: float = 1, 
            n_pts: int = 1000
            ) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(1/n_pts, 1, n_pts)
    y = 1/( 1+(1/x**a - 1)**k )
    return x, y