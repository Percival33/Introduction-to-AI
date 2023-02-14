#!/usr/bin/env python
import matplotlib.pyplot as plt

X = [1,3,5,8,10,11]

Y = [
    565.638,
    564.042,
    562.064,
    570.961,
    563.880,
    565.942
]

# X, Y = reversed(X), reversed(Y)

bar_width = 0.2
y_offset = 0

plt.bar(X, Y, bar_width, color='#0ca678')

plt.ylabel('śr wartości rozwiązań')
plt.xlabel('rozmiar elity')
plt.xlim(0,12)
plt.xticks(X, X, ha='center')
plt.axhline(y = 562.064, color = 'r', linestyle = '-')
plt.show()