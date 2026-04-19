Super Mario Bros Level 1
=============

An attempt to solve the first level of Super Mario Bros using a linear genetric programming algorithm.

![screenshot](https://raw.github.com/justinmeister/Mario-Level-1/master/screenshot.png)

Here I introduce an approach based on Genetic Algorithms (linear genetic programming) to learn the first level from the Mario AI simulator. 

Each instruction is encoded in a chromosome and after every generation altered by applying crossovers and mutations. 

Here you can find a video
https://youtu.be/il1BNu5ma-U showing one solution that the algorithm converged to.

run the file lgp_optimization.py to start training.

DEPENDENCIES:

Pygame 1.9.1 (Python 2)

Pygame 1.9.2 (Python 3) - a little trickier to get going.

To install dependencies for Python 2.x:

	pip install -r requirements.txt

## Docker Development Environment

Este projeto suporta desenvolvimento via Docker com suporte gráfico para o pygame.

### Pré-requisitos

- Docker e Docker Compose instalados
- Para suporte gráfico no Linux, execute antes:
  ```bash
  xhost +local:docker
  ```

### Comandos

**Construir e iniciar o container:**
```bash
docker-compose up -d
```

**Acessar o container:**
```bash
docker exec -it mario-lgp-dev bash
```

**Rodar o treinamento:**
```bash
docker exec -it mario-lgp-dev python lgp_optimization.py
```

**Rodar o jogo diretamente:**
```bash
docker exec -it mario-lgp-dev python mario_level_1.py
```

**Parar o container:**
```bash
docker-compose down
```

**Assistir um indivíduo da população:**
```bash
docker exec -i mario-lgp-dev python watch_mario.py lgp-test-run 0
```
Troque o 0 pelo número do indivíduo (0-5).