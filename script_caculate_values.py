from multiprocessing.pool import Pool
from quick_clique import run_quick_clique
import sys
from utils import get_existing_results, generate_graph
from random import shuffle
import glob
import os


def create_result_file_symmetry(file_name: str, op_file_name: str):
    f = open(file_name, 'r')
    elements = f.readline().split(" ")
    f.close()
    replaced_elements = []
    for ele in elements:
        if ele:
            replacement = ele.replace("2", "x")
            replacement = replacement.replace("0", "2")
            replacement = replacement.replace("x", "0")
            replaced_elements.append(replacement)
    with open(op_file_name, 'w') as f:
        f.write(" ".join(replaced_elements))


def append_results_symmetric_computation(existing_triplet_results):
    for n,n0,n2 in list(existing_triplet_results.keys()):
        if (n,n2,n0) not in existing_triplet_results:
            existing_triplet_results[(n,n2,n0)] = existing_triplet_results[(n,n0,n2)]
            g = glob.glob(f"./results/graph_{n}_{n0}_{n2}-*.txt")

            out_file_name =os.path.join(\
                "results",f"graph_{n}_{n2}_{n0}-{existing_triplet_results[(n,n0,n2)]}.txt")
            create_result_file_symmetry(g[0], out_file_name)


def generate_triplets(n: int, existing_triplet_results: dict = None):
    triplets = []
    for n in range(2, max_n + 1):
        for n0 in range(1, n):
            for n2 in range(1, n-n0+1):
                # print(n, n0, n2)
                if existing_triplet_results and (n, n0, n2) in existing_triplet_results: continue
                if existing_triplet_results and (n, n2, n0) in existing_triplet_results: continue
                # skipping for now, results should be added in the second run
                if (n, n2, n0) in triplets: continue
                triplets.append((n, n0, n2))
    return triplets



if __name__ == "__main__":
    existing_triplet_results = get_existing_results()

    args = sys.argv
    if len(args) > 1:
        try:
            max_n = int(args[1])
        except:
            max_n = 6
    else: max_n = 6

    triplets = generate_triplets(max_n, existing_triplet_results)
    
    # vertices, edges, vertex_map, reverse_vertex_map, mapped_edges = generate_graph(n, n0, n2)
    # can be sorted w.r.t num vertices also, change the index in key fn to 0
    print("Generating the triplet graph for sorting according to number of edges")
    triplets.sort(key=lambda trip: len(generate_graph(*trip)[1]))
    # shuffle(triplets)

    # for debugging only
    # for trip in triplets:
    #     run_quick_clique(*trip)

    with Pool(max(os.cpu_count() - 1, 1)) as pool:
        pool.starmap(run_quick_clique, triplets)

    # disabled for debugging, if running the binary is required using generated graph
    # if os.path.exists("graphs"):
    #     for file in glob.glob("graphs/*", recursive=True):
    #         os.remove(file)
    #     os.rmdir("graphs")
    
    existing_triplet_results = get_existing_results()

    # add already computed result for (n, n2, n0) if (n, n0, n2) exists to not repeat computations
    append_results_symmetric_computation(existing_triplet_results)