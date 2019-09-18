import sys
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

sample_size = int(sys.argv[1])
num_samples = int(sys.argv[2])
advantage = float(sys.argv[3])

win_count = [0, 0]

group1_mean_list = []
group2_mean_list = []

for i in range(num_samples):
	group1 = np.random.randint(1, 12, sample_size)
	group2 = np.random.randint(1, 12, sample_size) + advantage
	group1_mean = group1.mean()
	group2_mean = group2.mean()
	group1_mean_list.append(group1_mean)
	group2_mean_list.append(group2_mean)
	if group1_mean > group2_mean:
		win_count[0] += 1
		winner = "group1"
	else:
		win_count[1] += 1
		winner = "group2"
	print("{} {:0.3f} {:0.3f} {}".format(i, group1_mean, group2_mean, winner))
print("\nFinal Results:")
print("Group 1 Won: {:0.3f}".format(win_count[0]/num_samples))
print("Group 2 Won: {:0.3f}".format(win_count[1]/num_samples))

group1_means = np.array(group1_mean_list)
group2_means = np.array(group2_mean_list)

num_bins = 20

bins = np.linspace(0, 12, 100)

plt.hist(group1_means, bins, label='Group1')
plt.hist(group2_means, bins, label='Group2')
plt.legend(loc='upper right')
plt.show()