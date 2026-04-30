from saline_composite import SalineCompositeSimulation, SimulationConfig


def main() -> None:
    config = SimulationConfig()
    sim = SalineCompositeSimulation(config)
    sim.run()
    print("Simulation finished. Summary:")
    print(sim.get_summary_metrics())


if __name__ == "__main__":
    main()
