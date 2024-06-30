from utils import generate_graph, validate
import sys, subprocess, os
from datetime import datetime


def run_quick_clique(n, n0, n2):
    vertices, edges, vertex_map, reverse_vertex_map, mapped_edges = generate_graph(n, n0, n2)

    reverse_edges = set((b,a) for a,b in edges)

    all_edges = reverse_edges.union(edges)
    # write graph to file in custom format acc to: https://github.com/darrenstrash/quick-cliques

    file_name = f"graph_{n}_{n0}_{n2}"
    print(f"{file_name} has vertices: {len(vertices)}, edges(bidirectional): {len(all_edges)}")

    if not os.path.exists("graphs"):
        os.mkdir("graphs")

    with open(os.path.join("graphs",file_name), 'w') as f:
        f.write(f"{len(vertices)} {len(all_edges)}\n")
        f.writelines([f"{vertex_map[edge[0]]},{vertex_map[edge[1]]}\n" for edge in all_edges])

    # print("graph generation complete")
    start=datetime.now()

    algorithms = ["tomita", "adjlist", "degeneracy", "hybrid"]
    # call the compiled binary with the generated file as argument
    # TODO: add param to select algorithm
    s = subprocess.getstatusoutput(
        f"./quick-cliques/bin/qc --input-file={os.path.join('graphs',file_name)} \
            --algorithm={algorithms[0]}")
    if s[0]: print(f'Error: {s[1]}')
    
    # read the generated output to get the max_len clique
    max_len_clique = s[1].rstrip().lstrip()
    # print(max_len_clique)
    
    # remap the vertices back using the reverse_vertex_map
    max_len_clique_ele = [reverse_vertex_map[int(ele)] for ele in max_len_clique.split(" ")]
    print("Length, max clique for", file_name, len(max_len_clique_ele), max_len_clique_ele)
    if not validate(max_len_clique_ele):
        print("Error in algorithm. Invalid set:", max_len_clique_ele)
        exit(1)
    print(f"Max clique calculation time taken for {file_name}: {(datetime.now()-start) }")
    
    if not os.path.exists("results"):
        os.mkdir("results")

    # write max output to file
    with open(os.path.join("results", file_name + f"-{len(max_len_clique_ele)}.txt"), 'w') as f:
        f.write(" ".join(max_len_clique_ele))
    
    # TODO: disabled currently for running cpp program directly on generated graph
    # if os.path.exists(os.path.join("graphs",file_name)):
    #     os.remove(os.path.join("graphs",file_name))
    

if __name__ == "__main__":
    args = sys.argv

    try:
        if len(args) == 1:
            n = 10
            n0 = 1
            n2 = 3
        elif len(args) == 4:
            n = int(args[1])
            n0 = int(args[2])
            n2 = int(args[3])
        else: raise ValueError
        if n0 + n2 > n or n0<=0 or n2 <=0: raise ValueError
    except Exception as e:
        print(e, "\nInvalid input. Input Format: python find_good_string_group.py n n0 n2 \
              (s.t. n0 + n2 <= n and n0,n2 > 0)")
        exit()
    run_quick_clique(n, n0, n2)


    


