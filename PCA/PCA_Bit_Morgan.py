import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import matplotlib
import os

folder_path = r'C:\Users\Ellie\Documents\Chemistry\Year 3\Miniproject\Working Code for PCA\Bit Morgan Retry'
file_name = 'bit_morgan_pca_flattened.csv'
file_path = os.path.join(folder_path, file_name)


Data_pca = pd.read_csv(file_path)

test_data = Data_pca.iloc[[3, 7, 10, 12, 13, 17, 20, 25,
                           29, 30, 35, 55, 65, 66, 67, 68,
                           69, 70, 84, 89, 98, 99, 114, 126,
                           141, 150, 151, 152, 154, 163, 166,
                           169, 172, 178, 179, 180, 181, 183,
                           184, 188, 189, 198, 205, 206, 209,
                           214, 216, 223, 225, 228, 230, 234,
                           237, 243, 249, 251, 253, 259, 262,
                           266, 269, 279, 283, 285, 305, 307,
                           310, 311, 341],[0,1]]

train_data = Data_pca.drop(test_data.index, axis=0)
train_data = train_data.iloc[:, [0, 1]]

# Combine data for axis scaling
combined_data = np.vstack((train_data, test_data))

x_min, x_max = combined_data[:, 0].min(), combined_data[:, 0].max()
y_min, y_max = combined_data[:, 1].min(), combined_data[:, 1].max()

# Create plot
fig, ax = plt.subplots(figsize=(8, 6))
scatter_train = ax.scatter(train_data.iloc[:, 0], train_data.iloc[:, 1], color='black', label="Training Set", alpha=0.7)
scatter_test = ax.scatter(test_data.iloc[:, 0], test_data.iloc[:, 1], color='red', label="Testing Set", alpha=0.7)

# Set axis limits with padding
plt.xlim(x_min - 0.1, x_max + 0.1)
plt.ylim(y_min - 0.1, y_max + 0.1)

# Add axis labels, title, and legend
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Bit Morgan PCA Plot: Training vs Testing Sets")
plt.legend(loc="upper right")
plt.grid(True)
plt.axis("equal")
plt.savefig('bit_morgan_pca_full.png', dpi=300, bbox_inches='tight')

# Add hover functionality to display coordinates
annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", ha="center", fontsize=9,
                    bbox=dict(boxstyle="round", fc="w"))
annot.set_visible(False)

def update_annot(scatter, ind):
    print(f"Hovered indices: {ind}")
    if len(ind["ind"]) > 0:  # Check if ind contains any indices
        pos = scatter.get_offsets()[ind["ind"][0]]  # Get the first index
        print(f"Coordinates of hovered point: {pos}")
        annot.xy = pos
        annot.set_text(f"({pos[0]:.2f}, {pos[1]:.2f})")
        annot.set_visible(True)
def on_hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        for scatter in [scatter_train, scatter_test]:
            print(scatter.get_offsets())  # Check the coordinates of all points
            cont, ind = scatter.contains(event)
            print(f"cont: {cont}, ind: {ind}")
            if cont and len(ind["ind"]) > 0:  # Ensure there's at least one index
                update_annot(scatter, ind)
                fig.canvas.draw_idle()
                return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", on_hover)

# Show plot
plt.show()

# Coordinate lookup function
def find_nearest_point(data, x_input, y_input):
    distances = np.sqrt((data.iloc[:, 0] - x_input) ** 2 + (data.iloc[:, 1] - y_input) ** 2)
    nearest_idx = distances.idxmin()
    return nearest_idx

######
# Prompt for coordinates after closing the plot window
try:
    x_input = float(input("Enter X coordinate: "))
    y_input = float(input("Enter Y coordinate: "))
    nearest_index = find_nearest_point(Data_pca, x_input, y_input)
    print(f"Closest point index: {nearest_index}")
    print("Corresponding data:")
    print(Data_pca.iloc[nearest_index])
except ValueError:
    print("Invalid input! Please enter numeric coordinates.")


print("all done")
