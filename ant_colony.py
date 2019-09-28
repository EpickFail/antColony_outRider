import numpy as np


class Colony(object):

    def __init__(self, path, ants, bestAnts, count, decay, alpha=1, beta=1):
        self.path = path             # numpy.array - матрица смежности грифа, главная диогональ np.inf
        self.pheromone = np.ones(self.path.shape) / len(path)
        self.all_inds = range(len(path))
        self.ants = ants             # количество муравьев в итерации
        self.bestAnts = bestAnts     # количесвто муравьев, которые вносят феромон
        self.count = count           # количество итераций
        self.decay = decay           # коэффициент  угасания феромона
        self.alpha = alpha           # параметр феромона
        self.beta = beta             # параметр дистанции между вершинами

    # запускаем муравьев
    def Start(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.count):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.bestAnts, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone * self.decay
        return all_time_shortest_path

    # разносим феромон
    def spread_pheronome(self, all_paths, bestAnts, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:bestAnts]:
            for move in path:
                self.pheromone[move] += 1.0 / self.path[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for elem in path:
            total_dist += self.path[elem]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for j in range(self.ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = list()
        visited = set()
        visited.add(start)
        prev = start
        for k in range(len(self.path) - 1):
            move = self.pick_move(self.pheromone[prev], self.path[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move


pathStr = list(map(int, input().split()))
path = np.zeros((len(pathStr), len(pathStr)))
path[0] += pathStr
for s in range(1, len(pathStr)):
    pathStr = list(map(int, input().split()))
    path[s] += pathStr
for p in range(len(path)):
    path[p] = [int(item) for item in path[p]]
for i in range(len(path)):
    for j in range(len(path[i])):
        if path[i][j] == 0:
            path[i][j] = np.inf
ant_colony = Colony(path, 10, 1, 1000, 0.85, alpha=1, beta=1)
shortest_path = ant_colony.Start()
print(int(shortest_path[1]))
