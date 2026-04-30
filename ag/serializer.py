import pickle
import datetime
import populacao

def salvar_populacao(populacao, path):
    data = format_data(populacao)
    with open(path, "wb") as f:
        pickle.dump(data, f)

def carregar_populacao(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def format_data(populacao: populacao.Populacao):
    data = {
        "datetime":datetime.datetime.now(),
        "populacao": populacao,
        "melhor_individuo": populacao.pegar_melhor()
    }
    
    return data