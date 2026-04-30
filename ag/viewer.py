import os
import sys

# Adiciona o diretório raiz ao path para encontrar o pacote 'data'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import serializer

def exibir_resultados(path):
    if not os.path.exists(path):
        print(f"Erro: Arquivo '{path}' não encontrado.")
        return

    try:
        data = serializer.carregar_populacao(path)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return
    
    dt = data.get('datetime')
    dt_str = dt.strftime('%d/%m/%Y %H:%M:%S') if dt else "Desconhecido"
    
    print("\n" + "="*60)
    print(f" RESULTADOS DA POPULAÇÃO - {dt_str}")
    print("="*60)
    
    populacao = data.get("populacao")
    melhor = data.get("melhor_individuo")
    
    if not populacao:
        print("Nenhum dado de população encontrado no arquivo.")
        return

    print(f"Total de Indivíduos: {len(populacao.individuos)}")
    
    if melhor:
        print("\n🏆 MELHOR INDIVÍDUO:")
        print(f"  UUID:    {melhor.uuid}")
        print(f"  Fitness: {melhor.fitness}")
        print(f"  Genes:   {melhor.cromossomo}")
    else:
        print("\n⚠️ Nenhum 'melhor indivíduo' avaliado encontrado.")
    
    print("\n" + "-" * 60)
    print(f"{'Pos':<3} | {'UUID (Início)':<15} | {'Fitness':<10}")
    print("-" * 60)
    
    # Ordenar por fitness para exibição
    individuos_ordenados = sorted(
        populacao.individuos, 
        key=lambda x: x.fitness if x.fitness is not None else -float('inf'), 
        reverse=True
    )
    
    for i, ind in enumerate(individuos_ordenados):
        fitness_str = f"{ind.fitness:.2f}" if ind.fitness is not None else "N/A"
        uuid_short = str(ind.uuid)[:15] + "..."
        print(f"{i+1:<3} | {uuid_short:<15} | {fitness_str:<10}")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Tenta ler o arquivo passado por argumento ou o padrão 'populacao1'
    target_path = sys.argv[1] if len(sys.argv) > 1 else "populacao1"
    exibir_resultados(target_path)
