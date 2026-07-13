from coverage_planner.io import load_config,export_csv
from coverage_planner.planner import CoveragePlanner
from coverage_planner.visualization import MissionVisualizer
from coverage_planner.analyzer import CoverageAnalyzer

cfg = load_config("config/planner.yaml")

planner = CoveragePlanner(cfg)
missions = planner.generate()

MissionVisualizer(cfg).plot(
    missions,
    show_waypoint=True,
    show_arrow=True,
)

export_csv(
    missions,
    "output",
)

analyzer = CoverageAnalyzer(cfg)
coverage = analyzer.analyze(missions)
analyzer.statistics(coverage, missions)
analyzer.plot(coverage)