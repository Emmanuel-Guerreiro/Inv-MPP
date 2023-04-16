from typing import List, Set

import numpy as np
import numpy.typing as npt

# Initial pheromones: Pn = zeros(n)

# Visited cities can be represented with a
# len(S) array. Where Vi = 1 if visited, 0 if not
# This will keep track of S = S − {j} where j is the selected

# Initial distances
# randInt(3,3)


EVAPORTAION_RATE = 0.5


def range_inc(start, stop):
    i = start
    while i < stop:
        yield i
        i += 1


class ArtificialAnt:
    def __init__(
        self,
        nCities: int,
        distances: npt.NDArray,
        pheromones: npt.NDArray,
        initialCity: int,
    ):
        self.initial = initialCity
        self.path = [initialCity]
        self.current = self.initial
        self.visited = self.initialize_visited(nCities)
        self.pheromones = pheromones
        self.distances = distances
        return

    def initialize_visited(self, nCities: int) -> npt.NDArray:
        return np.zeros(nCities)

    # def initialize_path(self, nCities: int) -> npt.NDArray:
    #     return np.zeros(nCities)

    def select_next_node(self) -> int:
        av_idx = []
        for i in range(len(self.visited)):
            if self.visited[i] == 0:
                av_idx.append(i)

        if len(av_idx) == 1:
            return av_idx[0]

        ph_from_current = self.pheromones[self.current]
        sum_Tij = 0
        for i in av_idx:
            sum_Tij += ph_from_current[i]

        prob = []
        test_pij = 0
        for idx in av_idx:
            pij = ph_from_current[idx] / sum_Tij
            test_pij += pij
            prob.append(pij)
        ch = np.random.choice(av_idx, p=prob)
        return int(ch)

    def inc_pheromones(self, position: Set[int]):
        p = self.pheromones.item(position) + float(1)
        self.pheromones.itemset(position, p)

    def move(self, next_city: int):
        # A priori, no parece que haga falta incrementar pheromones
        # En el recorrido de la misma hormiga.
        # self.inc_pheromones((self.current, next_city))
        self.visited.itemset(self.current, 1)
        self.current = next_city
        self.path.append(self.current)

    def run(self):
        while len(self.path) < len(self.visited):
            next = self.select_next_node()
            self.move(next)

        # Will end the path going back to the initial
        self.move(self.initial)
        return self.path


class AntSystem:
    def __init__(self, noc: int, updt: int = 4, s: str = "S"):
        self.nCities = noc
        self.distances = self.initialize_distances(noc, strategy=s)
        self.pheromones = self.initialize_pheromones(noc)
        self.initial_pool = list(range_inc(0, self.nCities))
        self.shortest_path: dict = {"d": float("inf"), "p": []}
        self.update_every = updt
        self.historic_distances = []
        return

    def initialize_distances(self, noc: int, strategy: str = "S"):
        """
        strategy:
            S: Symetric distances. The problem will be STP
            A: Asymetric distances. The problem will be ASTP
        """
        d = np.random.randint(0, 100, size=(noc, noc))
        if strategy == "S":
            m = np.tril(d, k=-1)
            n = m.transpose()
            return np.add(m, n)
        return d

    def calc_path_distance(self, path: List[int]) -> int:
        tot = 0
        for i in range(len(path) - 1):
            tot += self.distances.item((path[i], path[i + 1]))
        return tot

    def initialize_pheromones(self, noc: int):
        p = np.ones(shape=(noc, noc))
        for i in range(noc):
            p.itemset((i, i), 0)
        return p

    def evaporate(self):
        self.pheromones *= EVAPORTAION_RATE
        pass

    def save_shortest(self, path: List[int]):
        n_p = self.calc_path_distance(path)

        ## Will save all the values for the plot
        ## Is a test
        self.historic_distances.append(n_p)

        if n_p < self.shortest_path["d"]:
            self.shortest_path["d"] = n_p
            self.shortest_path["p"] = path

        return

    def reset_shortest(self):
        self.shortest_path = {"d": float("inf"), "p": []}

    def pheromone_intensification(self, idx):
        p = self.shortest_path["p"]
        for i in range(len(p) - 1):
            position = (p[i], p[i + 1])
            updated = self.pheromones.item(position) + (1 / self.shortest_path["d"])
            self.pheromones.itemset(position, updated)
        return

    def increment_pheromones(self, idx: int):
        # Cada 1/4 de las hormigas totales se actualiza
        p = self.shortest_path["p"]
        for i in range(len(p) - 1):
            position = (p[i], p[i + 1])
            incremented = self.pheromones.item(position) + 1
            self.pheromones.itemset(position, incremented)
        return

    def run(self, iteration: int):
        for i in range(iteration):
            path = ArtificialAnt(
                initialCity=np.random.choice(self.initial_pool),
                nCities=self.nCities,
                distances=self.distances,
                pheromones=self.pheromones,
            ).run()
            self.save_shortest(path)
            if i % self.update_every == 0:
                self.evaporate()
                self.increment_pheromones(i)
                self.pheromone_intensification(i)
                self.reset_shortest()

        print(self.shortest_path)
        print(self.distances)
        return
