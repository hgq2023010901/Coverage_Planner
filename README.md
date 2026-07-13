# Multi-UAV Coverage Planner

A lightweight multi-UAV coverage path planner for rectangular search areas.

The planner generates complete lawnmower-style trajectories for multiple UAVs, redistributes lanes across subregions, exports CSV missions, and provides both path visualization and coverage analysis.

---

## Features

- Multi-UAV rectangular area decomposition
- Boustrophedon coverage path generation
- Lane redistribution based on camera footprint and overlap
- Waypoint interpolation for long segments
- YAML configuration loading
- CSV mission export
- Matplotlib path visualization
- Coverage heatmap and statistics

---

## Planning Flow

The current planner follows this flow:

1. Split the search area into equal-width subregions.
2. Compute the camera footprint from flight altitude and FOV.
3. Compute an effective lane width using the configured overlap.
4. Distribute lanes uniformly inside each subregion.
5. Generate a snake-like trajectory for each drone.
6. Interpolate long segments into waypoint sequences.
7. Export missions to CSV if needed.

---

## Camera Model

The camera footprint is derived from altitude and field of view:

Horizontal footprint:

```
Width = 2H tan(HFOV / 2)
```

Vertical footprint:

```
Height = 2H tan(VFOV / 2)
```

The effective lane area is then computed as:

```
Effective Lane Width  = Footprint Width × (1 − Overlap)
Effective Lane Height = Footprint Height × (1 − Overlap)
```

where:

- H is the flight altitude
- HFOV is the horizontal field of view
- VFOV is the vertical field of view
---

## Project Structure

```
Coverage_Planner/
├── config/
│   └── planner.yaml
├── coverage_planner/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── io.py
│   ├── models.py
│   ├── planner.py
│   └── visualization.py
├── main.py
├── output/
└── README.md
```

---

## Configuration

The default configuration is stored in [config/planner.yaml](config/planner.yaml).

Example:

```yaml
area:
  width: 24.384
  length: 91.44

camera:
  hfov: 90
  vfov: 90
  overlap: 0.10

flight:
  altitude: 1.5
  speed: 1
  waypoint_spacing: 5

drone_num: 4
```

Supported fields:

- `area.width`
- `area.length`
- `camera.hfov`
- `camera.vfov`
- `camera.overlap` (optional, default `0.10`)
- `flight.altitude`
- `flight.speed`
- `flight.waypoint_spacing` (optional, default `20`)
- `drone_num`

---

## Usage

### Run the main

```bash
python main.py
```

The code loads `config/planner.yaml`, generates missions, visualizes the paths, exports CSV files under `output/`, and prints coverage statistics.

### Programmatic use

```python
from coverage_planner.io import load_config, export_csv
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

export_csv(missions, "output")

analyzer = CoverageAnalyzer(cfg)
coverage = analyzer.analyze(missions)
analyzer.statistics(coverage, missions)
analyzer.plot(coverage)
```

### Direct model construction

```python
from coverage_planner.models import CameraConfig, FlightConfig, PlannerConfig, SearchArea
from coverage_planner.planner import CoveragePlanner

cfg = PlannerConfig(
    area=SearchArea(width=80.0, length=400.0),
    camera=CameraConfig(hfov=84.0, vfov=63.0, overlap=0.10),
    flight=FlightConfig(altitude=20.0, speed=5.0, waypoint_spacing=20.0),
    drone_num=4,
)

missions = CoveragePlanner(cfg).generate()
```

---

## Output

Each drone mission is represented by a list of waypoints with:

- `id`
- `x`
- `y`
- `z`
- `yaw`
- `speed`

The CSV export writes one file per drone, for example `output/drone_0.csv`. Each file contains the generated waypoints plus a final return-to-start row.

---

## Visualization

The visualization module can show:

- Search area outline
- Subregion boundaries
- Flight trajectories
- Waypoints
- Direction arrows
- Camera footprint overlays

The analyzer module can compute:

- Coverage ratio
- Overlap ratio
- Missed area
- Total waypoint count
- Approximate flight distance
- Estimated flight time

---

## Future Work

- Polygon coverage
- No-fly zones
- Dynamic replanning
- Terrain following
- Online coverage verification
- PX4/QGroundControl mission export
- Cooperative multi-UAV planning

---

## License

MIT License