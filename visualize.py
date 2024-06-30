import matplotlib.pyplot as plt
from utils import get_existing_results
import sys

def visaluze_matplot3d(path_folder):
    print("generating graph")
    path_to_result_file_pattern = f"./{'results' if path_folder is None else path_folder}/*.txt"
    existing_triplet_results = get_existing_results(path_to_result_file_pattern)
    # max_n = max([triplet[0] for triplet in existing_triplet_results.keys()])
    # print(existing_triplet_results)

    x = []
    y = []
    z = []
    vals = []
    for trip, value in existing_triplet_results.items():
        n, n0, n2 = trip
        x.append(n)
        y.append(n0)
        z.append(n2)
        vals.append(value)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('n')
    ax.set_ylabel('n0')
    ax.set_zlabel('n2')
    scatter = ax.scatter(x, y, z, c=vals, cmap='viridis', s=30)  # Use a colormap of your choice maybe 'jets' or 'viridis'
    cbar = plt.colorbar(scatter)
    cbar.set_label('P function')
    for i in range(len(x)):
        ax.text(x[i], y[i], z[i], f'{vals[i]}', color='black', fontsize=8)
    plt.show()


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        path_folder = args[1]
    path_folder = None
    visaluze_matplot3d(path_folder)