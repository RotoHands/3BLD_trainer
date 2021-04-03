import pickle

def load_algs_dict(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def update_basic_statics(algs_dict):
    for index in algs_dict:
        algs_dict[index].solves_times = []
    with open("algs_dict.pkl", "wb") as f:
        pickle.dump(algs_dict, f)

algs_dict = load_algs_dict("algs_dict.pkl")
update_basic_statics(algs_dict)