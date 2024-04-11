import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

mu1 = 305.57143
variance1 = 195077.29

mu2 = 573.46377
variance2 = 1158220.4

mu3 = 422.02128
variance3 = 233511.85


sigma1 = math.sqrt(variance1)
x1 = np.linspace(mu1 - 3*sigma1, mu1 + 3*sigma1, 100)
ya = stats.norm.pdf(x1, mu1, sigma1)

sigma2 = math.sqrt(variance2)
x2 = np.linspace(mu2 - 3*sigma2, mu2 + 3*sigma2, 100)
yb = stats.norm.pdf(x2, mu2, sigma2)

sigma3 = math.sqrt(variance3)
x3 = np.linspace(mu3 - 3*sigma3, mu3 + 3*sigma3, 100)
yc = stats.norm.pdf(x3, mu3, sigma3)

plt.plot(x1, ya)
plt.plot(x2,yb)
plt.plot(x3, yc)

##Pond = green
##Rattle =
plt.show()