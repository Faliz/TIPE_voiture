import imageio
import matplotlib.pyplot as plt

im = imageio.imread("circuit.jpg")

"""for i in range(len(im[0])):
    for j in range(len(im)):
        if im[j][i][0] == 0:
            plt.scatter(i,-j)"""
            
print(type(im))
plt.show()