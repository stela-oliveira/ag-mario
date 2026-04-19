import pickle

def save_checkpoint(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_checkpoint(path):
    with open(path, "rb") as f:
        return pickle.load(f)