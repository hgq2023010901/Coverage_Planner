from coverage_planner.models import *

cfg = PlannerConfig(
    area=SearchArea(
        width=80.0,
        length=400.0,
    ),

    camera=CameraConfig(
        hfov=84.0,
        vfov=63.0,
        overlap=0.10,
    ),

    flight=FlightConfig(
        altitude=20.0,
        speed=5.0,
        waypoint_spacing=20.0,
    ),

    drone_num=4,
)

from coverage_planner.planner import CoveragePlanner

planner = CoveragePlanner(cfg)

missions = planner.generate()

print(missions)