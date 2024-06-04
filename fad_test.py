import matplotlib.pyplot as plt

models = ['1M', '10M', '58M', '200M', '300M', '300M_official']
scores = [8.19, 7.09, 6.12, 10.83, 9.40, 1.81]



plt.bar(models, scores)

plt.suptitle('FAD')
plt.show()