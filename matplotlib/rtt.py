import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Min RTT (ms)', 'Avg RTT (ms)', 'Max RTT (ms)', 'Mdev RTT (ms)']
attempt1 = [9.546, 14.524, 19.726, 2.895]
attempt2 = [9.787, 14.787, 19.533, 2.875]
attempt3 = [9.684, 14.593, 19.516, 2.834]

bar_width = 0.25  # Width of the bars
index = np.arange(len(categories))  # Index for categories

# Plotting
plt.figure(figsize=(10, 6))

# Create bars for each attempt
plt.bar(index, attempt1, width=bar_width, label='Attempt 1')
plt.bar(index + bar_width, attempt2, width=bar_width, label='Attempt 2')
plt.bar(index + 2 * bar_width, attempt3, width=bar_width, label='Attempt 3')

# Adding Xticks
plt.xlabel('RTT Statistics', fontsize=12)
plt.ylabel('Milliseconds (ms)', fontsize=12)
plt.xticks(index + bar_width, categories, fontsize=10)
plt.title('Comparison of RTT Statistics Across Attempts')
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()