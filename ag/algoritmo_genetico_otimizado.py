import random
from individuo import Individuo
from populacao import Populacao
from data.tools import keybinding

class AlgoritmoGeneticoOtimizado:
    """
    Implementação de Algoritmo Genético com Janela Deslizante (Sliding Window)
    otimizado para o Super Mario Bros (1-1).
    Versão 2.0: Suporta combinações de teclas e mutação adaptativa.
    """
    def __init__(self, tamanho_populacao=20, tamanho_janela=10, genes_para_fixar=2):
        self.tamanho_populacao = tamanho_populacao
        self.tamanho_janela = tamanho_janela  # Número de pares (comando, duração)
        self.genes_para_fixar = genes_para_fixar # Quantos genes da janela ativa movem para o prefixo
        
        self.prefixo_fixo = [] # [cmd, dur, cmd, dur, ...]
        self.janela_ativa = self._gerar_genes_aleatorios(self.tamanho_janela)
        
        self.populacao = Populacao()
        self.geracao_atual = 0
        self.melhor_fitness_global = -1
        self.historico_fitness = []
        self.estabilidade_fitness = 0
        self.limite_estabilidade = 10 # Aumentado para dar mais tempo de exploração
        
    def _gerar_genes_aleatorios(self, n_genes):
        """Gera comandos inteligentes, priorizando movimento e pulo."""
        genes = []
        possible_keys = [
            keybinding['right'],
            keybinding['right'] | keybinding['jump'],
            keybinding['right'] | keybinding['action'],
            keybinding['right'] | keybinding['jump'] | keybinding['action'],
            keybinding['jump'],
            keybinding['still']
        ]
        for _ in range(n_genes):
            genes.append(random.choice(possible_keys))
            genes.append(random.randint(50, 150))
        return genes

    def inicializar_populacao(self):
        """Cria uma nova população baseada no melhor indivíduo e mutações."""
        self.populacao.limpar()
        
        # 1. Elitismo: Mantém o melhor indivíduo sem alterações
        self.populacao.add_individuo(Individuo(self.prefixo_fixo + self.janela_ativa))
        
        # 2. Mutações e Crossover
        for _ in range(self.tamanho_populacao - 1):
            if random.random() < 0.2 and len(self.populacao.individuos) > 1:
                # Crossover simples entre dois aleatórios (se houver mais de um)
                ind1 = random.choice(self.populacao.individuos)
                ind2 = Individuo(self.prefixo_fixo + self._mutar_janela(self.janela_ativa))
                novo_cromossomo = self._crossover(ind1.cromossomo, ind2.cromossomo)
                self.populacao.add_individuo(Individuo(novo_cromossomo))
            else:
                # Mutação pura
                cromossomo_mutado = self._mutar_janela(self.janela_ativa)
                self.populacao.add_individuo(Individuo(self.prefixo_fixo + cromossomo_mutado))

    def _mutar_janela(self, janela):
        """Aplica mutação na janela ativa. A agressividade aumenta com a estabilidade."""
        nova_janela = janela.copy()
        
        # Taxa de mutação adaptativa
        taxa_mutacao_gene = 0.2
        if self.estabilidade_fitness > (self.limite_estabilidade // 2):
            taxa_mutacao_gene = 0.5 # Aumenta exploração se estiver travado
            
        for i in range(self.tamanho_janela):
            if random.random() < taxa_mutacao_gene:
                pos = i * 2
                if random.random() < 0.6:
                    # Muda o comando usando o gerador inteligente
                    nova_janela[pos] = self._gerar_genes_aleatorios(1)[0]
                else:
                    # Muda a duração
                    alteracao = random.randint(-40, 40)
                    nova_janela[pos+1] = max(30, min(300, nova_janela[pos+1] + alteracao))
                
        return nova_janela

    def _crossover(self, cromossomo1, cromossomo2):
        """Realiza um crossover de um ponto na parte da janela ativa."""
        # Apenas cruza a parte da janela ativa (após o prefixo)
        idx_prefixo = len(self.prefixo_fixo)
        janela1 = cromossomo1[idx_prefixo:]
        janela2 = cromossomo2[idx_prefixo:]
        
        ponto_corte = random.randint(1, self.tamanho_janela - 1) * 2
        nova_janela = janela1[:ponto_corte] + janela2[ponto_corte:]
        
        return self.prefixo_fixo + nova_janela

    def avaliar_populacao(self):
        for ind in self.populacao.individuos:
            if ind.fitness is None:
                # O usuário agora prefere redraw=True para acompanhar
                ind.calcular_fitness(redraw=True)

    def evoluir(self, n_geracoes=1):
        for _ in range(n_geracoes):
            self.geracao_atual += 1
            print(f"\n--- Geração {self.geracao_atual} (Prefixo: {len(self.prefixo_fixo)//2} genes) ---")
            
            self.inicializar_populacao()
            self.avaliar_populacao()
            
            melhor_ind = self.populacao.pegar_melhor()
            fitness_atual = melhor_ind.fitness
            
            print(f"Melhor Fitness da Geração: {fitness_atual} (Global: {self.melhor_fitness_global})")
            
            # Salva histórico
            self.historico_fitness.append({'geracao': self.geracao_atual, 'fitness': fitness_atual})
            import json, os
            caminho = os.path.join(os.path.dirname(__file__), '..', 'historico_sem_paralelismo.json')
            with open(caminho, 'w') as f:
                json.dump(self.historico_fitness, f)
            
            # Verifica progresso
            if fitness_atual > self.melhor_fitness_global:
                self.melhor_fitness_global = fitness_atual
                self.janela_ativa = melhor_ind.cromossomo[len(self.prefixo_fixo):]
                self.estabilidade_fitness = 0
                print(f"Novo Recorde! Fitness: {self.melhor_fitness_global}")
            else:
                self.estabilidade_fitness += 1
                
            # Critério para Avançar a Janela
            if self.estabilidade_fitness >= self.limite_estabilidade:
                self.avancar_janela()

    def avancar_janela(self):
        print(f">>> Estabilidade em {self.estabilidade_fitness}. Avançando Janela Deslizante...")
        
        # 1. Integra os primeiros genes da janela ativa ao prefixo fixo
        n_bytes_fixar = self.genes_para_fixar * 2
        genes_para_integrar = self.janela_ativa[:n_bytes_fixar]
        self.prefixo_fixo.extend(genes_para_integrar)
        
        # 2. Desliza a janela: remove os fixados e adiciona novos genes ao final
        nova_janela = self.janela_ativa[n_bytes_fixar:]
        novos_genes = self._gerar_genes_aleatorios(self.genes_para_fixar)
        self.janela_ativa = nova_janela + novos_genes
        
        # 3. CRÍTICO: Reset de métricas para focar no novo segmento
        # Resetar a fitness global permite que o algoritmo foque em progredir a partir daqui
        self.estabilidade_fitness = 0
        self.melhor_fitness_global = -1 
        
        print(f"Janela Deslizada. Novo tamanho do Prefixo: {len(self.prefixo_fixo)//2} genes.")

    def salvar_melhor(self, nome_arquivo="melhor_mario"):
        import serializer as s
        melhor = self.populacao.pegar_melhor()
        if melhor:
            s.salvar_populacao(Populacao([melhor]), nome_arquivo)
            print(f"Melhor indivíduo salvo em {nome_arquivo}")

if __name__ == "__main__":
    ag = AlgoritmoGeneticoOtimizado(tamanho_populacao=15, tamanho_janela=10, genes_para_fixar=2)
    while True:
        ag.evoluir(1)
