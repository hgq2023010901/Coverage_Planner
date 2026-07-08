from __future__ import annotations

import csv
import yaml
from pathlib import Path

from .models import *


# ==========================================================
# Config
# ==========================================================

def load_config(path: str) -> PlannerConfig:

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(path)

    with open(path,"r") as f:

        data = yaml.safe_load(f)

    if data is None:

        raise RuntimeError(
            "planner.yaml is empty."
        )

    cfg = PlannerConfig(

        area=SearchArea(
            width=data["area"]["width"],
            length=data["area"]["length"],
        ),

        camera=CameraConfig(
            hfov=data["camera"]["hfov"],
            vfov=data["camera"]["vfov"],
            overlap=data["camera"].get(
                "overlap",
                0.1,
            ),
        ),

        flight=FlightConfig(
            altitude=data["flight"]["altitude"],
            speed=data["flight"]["speed"],
            waypoint_spacing=data["flight"].get(
                "waypoint_spacing",
                20,
            ),
        ),

        drone_num=data["drone_num"],

    )

    return cfg


# ==========================================================
# CSV Export
# ==========================================================

def export_csv(
    missions: list[DroneMission],
    output_dir: str,
):

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    for existing_file in output_path.iterdir():
        if existing_file.is_file():
            existing_file.unlink()

    

    for mission in missions:

        filename = output_path / f"drone_{mission.drone_id}.csv"

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "id",
                "x",
                "y",
                "z",
                "yaw",
                "speed",
            ])

            for wp in mission.waypoints:

                writer.writerow([
                    wp.id,
                    wp.x,
                    wp.y,
                    wp.z,
                    "" if wp.yaw is None else wp.yaw,
                    wp.speed,
                ])
                
            '''Return to the starting point'''
            writer.writerow([
                mission.waypoints[-1].id + 1,
                mission.waypoints[0].x,
                mission.waypoints[0].y,
                mission.waypoints[0].z,
                "" if mission.waypoints[0].yaw is None else mission.waypoints[0].yaw,
                mission.waypoints[0].speed,
            ])

    print(f"Exported to {output_dir}")
    print(f"Exported {len(missions)} missions.")
    print(f"Export Filenames: {[f'drone_{mission.drone_id}.csv' for mission in missions]}")