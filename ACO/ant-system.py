# TODO:
# [] Clean code
# [] Handle go back to the initial node

import random
from typing import List, Set

import numpy as np
import numpy.typing as npt

decrement_factor = 0.5
max_iter = 1000


class ArtificialAnt:
    def __init__(self, initial_node: int, non: int):
        self.initial = initial_node
        self.current = initial_node
        self.visited_nodes: dict[int, int] = self.init_visited_nodes(
            nodes_amount=non, initial=initial_node
        )
        self.path = [initial_node]
        return

    def init_visited_nodes(self, nodes_amount: int, initial: int):
        v_nodes = {}
        for i in range(nodes_amount):
            v_nodes[i] = 0

        v_nodes[initial] = 1
        return v_nodes

    def not_visited_nodes(self) -> List[int]:
        nv_nodes = []
        for n in self.visited_nodes:
            if self.visited_nodes[n] == 0:
                nv_nodes.append(n)
        return nv_nodes

    def mark_visited(self, n):
        self.visited_nodes[n] = 1
        return

    def deposit_pheromone(self, position: Set[int], pheromones: npt.NDArray):
        # Is correct to increment by 1?
        inc_value = pheromones.item(position) + 1
        pheromones.itemset(position, inc_value)
        return

    def choose_next_node(self, valid_nodes):
        # This strategy can be improved
        return random.choice(valid_nodes)

    def move_to_specific(self, source: int, objective: int, pheromones: npt.NDArray):
        self.current = objective
        self.mark_visited(self.current)
        self.path.append(self.current)
        self.deposit_pheromone((source, objective), pheromones)
        return

    def move(self, pheromones: npt.NDArray):
        nv_nodes = self.not_visited_nodes()
        # print(f"{nv_nodes}")
        if len(nv_nodes) == 0:
            self.move_to_specific(
                source=self.current, objective=self.initial, pheromones=pheromones
            )
            print("\n--------------------")
            print(f"Initial node: {self.initial}")
            print(f"Path realized: {self.path}")

            return (False, self.path)

        next_node = self.choose_next_node(nv_nodes)

        old_node = self.current
        self.current = next_node

        self.mark_visited(self.current)
        self.path.append(self.current)

        # print(f"Move realized: {old_node} -> {self.current}")
        # print(f"{pheromones }")

        self.deposit_pheromone((old_node - 1, self.current - 1), pheromones)

        # print("\n\n-----------------------\n")
        return (True, [])


class AntSystem:
    def __init__(self, non):
        # noc => number_of_nodes
        # self.pheromone = np.zeros_like(distances)
        self.nodes_amount = non
        self.nodes_list = []
        self.distances = np.random.randint(0, 100, size=[non, non])
        self.pheromone = self.init_pheromones(non)
        return

    def init_pheromones(self, noc):
        # Pheromones initialization strategy can be better
        return np.random.randint(0, 10, size=[noc, noc])

    def fitness_function(self):
        # How can i define a fitness function?
        return 0

    def update_pheromones(self):
        ## Decrement factor can be better
        factor = 1 - decrement_factor + decrement_factor * self.fitness_function()
        self.pheromone = self.pheromone * factor
        return

    def generate_initial_node(self):
        # Will pick a node from the possible values

        # If the list of possible nodes has been already used,
        # will pick from there
        list = self.nodes_list

        # If the list is not initialized yet, will create the possible
        if len(self.nodes_list) == 0:
            for i in range(self.nodes_amount):
                list.append(i)

        # Cache avalable nodes
        self.nodes_list = list
        return random.choice(list)

    def path_distance(self, path: List[int]):
        total = 0
        for i in range(len(path) - 1):
            total += self.distances.item((path[i], path[i + 1]))
        return total

    def run(self, noa: int):
        print(self.distances)
        for _ in range(noa):
            inode = self.generate_initial_node()
            ant = ArtificialAnt(initial_node=inode, non=self.nodes_amount)
            didnt_finish = True
            returned_path = []
            while didnt_finish:
                result = ant.move(self.pheromone)
                didnt_finish = result[0]
                returned_path = result[1]

            print(
                f"Distance: {self.path_distance(returned_path)} \n-------------------- \n"
            )
        self.update_pheromones()
        # print(f"{self.pheromone}")
        return


if __name__ == "__main__":
    AntSystem(non=10).run(10)
