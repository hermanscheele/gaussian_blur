import numpy as np
import matplotlib.pyplot as plt

sigx = 3.5
sigy = 3.5

def plt_gauss(sigx:float, sigy:float) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    x,y = np.meshgrid(x,y)

    def gaussian(x:float, y:float, sigx:float, sigy:float) -> float:
        return np.exp(-(((x**2) / (2*sigx**2)) + ((y**2) / (2*sigy**2))))

    ax.plot_surface(x, y, gaussian(x,y,sigx,sigy), color='lightgreen', alpha=0.9)
    plt.show()
     


# plt_gauss(sigx,sigy)