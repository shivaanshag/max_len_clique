import glob
import os
from itertools import permutations

def get_key_val_from_result_file(file_name: str):
    main = file_name.split(".")[1] # remove /. and .txt
    main = main.split(os.path.sep)[-1] # get graph_n_n0_n2-result
    res = int(main.split("-")[-1]) # get result
    trip = main.split("-")[0] # remove the -result
    triplet = trip.split("_")[1:] # get [n, n0, n2]
    triplet = tuple([int(x) for x in triplet]) # convert to int
    return triplet, res


def get_existing_results(pattern: str = "./results/*.txt"):
    g = glob.glob(pattern)
    existing_triplet_results = {}
    for file_name in g:
        triplet, result = get_key_val_from_result_file(file_name)
        existing_triplet_results[triplet] = result
    return existing_triplet_results

def validate(test):
    for ele in test:
        for e in test:
            if e == ele: continue
            if not good_distance(e, ele): return False
    return True


def good_distance(s1: str, s2: str):
    for j in range(len(s1)):
        if s1[j] == '2' and s2[j] == '0' or s1[j] == '0' and s2[j] == '2': return True
    return False


def generate_graph(n: int, n0: int, n2: int):
    try:
        if n0 + n2 > n or n0<=0 or n2 <=0: raise ValueError
    except Exception as e:
        print(e, "\nInvalid input. Input Format: python find_good_string_group.py n n0 n2 (s.t. n0 + n2 <= n and n0,n2 > 0)")
        exit()

    init_string = '0' * n0 + '2' * n2 + '1' * (n - n0 - n2)

    def generate_valid_comb(string:str):
        valid_comb = set()
        for iter_ in permutations(list(string)):
            new_comb = "".join(iter_)
            if len(new_comb) > len(string):
                print(new_comb)
                return
            if good_distance(string, new_comb):
                valid_comb.add(new_comb)

        return valid_comb

            
    # print("Generating graph for n, n2, n0:", n, n2, n0)

    vertices = generate_valid_comb(init_string)
    vertices.add(init_string)
    # file_name = 'graph_' + 'n_{}_n0_{}_n2_{}'.format(n, n0, n2) + '.cols'

    # print(vertices)
    vertex_map = {}
    reverse_vertex_map = {}
    i = 0
    for v in vertices:
        vertex_map[v] = i
        reverse_vertex_map[i] = v
        i +=1

    # print(vertices)

    # custom format edges
    edges = set()
    for v1 in vertices:
        for v2 in vertices:
            if v1 == v2: continue
            if good_distance(v1, v2):
                edges.add(tuple(sorted([v1, v2])))
    
    # print(edges)
    mapped_edges = []
    for f, to in edges:
        mapped_edges.append((vertex_map[f], vertex_map[to]))

    return vertices, edges, vertex_map, reverse_vertex_map, mapped_edges
   