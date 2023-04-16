from ACO.main import AntSystem
from uglyplotter.plot import Plot

if __name__ == "__main__":

    antsys = AntSystem(noc=20, updt=10000)
    antsys.run(10)

    distances = antsys.historic_distances

    Plot(
        title="Distances",
        xlabel="Iteration",
        ylabel="Distance",
        x=[i for i in range(len(distances))],
        values=[{"label": "Distances", "values": distances}],
    ).show()
