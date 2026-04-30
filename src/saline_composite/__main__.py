from . import SalineCompositeSimulation, SimulationConfig


def main() -> None:
    sim = SalineCompositeSimulation(SimulationConfig())
    sim.run()
    print(sim.get_summary_metrics())


if __name__ == "__main__":
    main()
