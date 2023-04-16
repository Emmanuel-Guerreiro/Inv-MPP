from typing import Any, Dict, List

import matplotlib.pyplot as plt


class Plot:
    def __init__(
        self,
        title: str,
        xlabel: str,
        ylabel: str,
        x: List,
        values: List[Dict[str, Any]],
    ):
        self.ax = plt.subplots()[1]
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.plot(x, values)

    def plot(self, x: List, v: List[Dict[str, Any]]):
        print(v)
        for y in v:
            self.ax.plot(x, y["values"], label=y["label"])
        return

    def show(self):
        plt.show()
        return

    def save(self, path: str):
        import os

        save_path = os.getcwd() + "/" + path
        plt.savefig(save_path)
        return
