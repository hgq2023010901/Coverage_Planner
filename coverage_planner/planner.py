from __future__ import annotations

import math
from typing import List

from .models import *


class CoveragePlanner:

    def __init__(self, config: PlannerConfig):

        self.cfg = config

    # =====================================================
    # Public API
    # =====================================================

    def generate(self) -> List[DroneMission]:

        lane_positions = self._compute_lane_positions()

        missions = []

        for drone_id, lanes in enumerate(lane_positions):

            mission = self._generate_single_drone(
                drone_id,
                lanes
            )

            missions.append(mission)

        return missions

    # =====================================================
    # Lane Planning
    # =====================================================

    def _compute_lane_positions(self):

        cfg = self.cfg

        sub_width = cfg.area.width / cfg.drone_num

        effective_lane = cfg.camera.effective_lane_width(
            cfg.flight.altitude
        )

        result = []

        for drone in range(cfg.drone_num):

            xmin = drone * sub_width

            lane_num = max(
                1,
                math.ceil(sub_width / effective_lane)
            )

            if lane_num % 2 == 1:

                lane_num += 1

            interval_num = lane_num - 1

            spacing = sub_width / interval_num

            lanes = [
                xmin + i * spacing
                for i in range(lane_num)
            ]

            result.append(lanes)

        return result

    # =====================================================
    # Single Drone
    # =====================================================

    def _generate_single_drone(
        self,
        drone_id: int,
        lanes: List[float]
    ) -> DroneMission:

        mission = DroneMission(
            drone_id=drone_id,
            start_x=lanes[0],
            end_x=lanes[-1]
        )

        top = self.cfg.area.length
        bottom = 0.0

        control_points = []

        upward = True

        for i, x in enumerate(lanes):

            # ---------- Vertical ----------
            if upward:

                control_points.append((x, bottom))
                control_points.append((x, top))

            else:

                control_points.append((x, top))
                control_points.append((x, bottom))

            # ---------- Horizontal ----------
            if i != len(lanes) - 1:

                next_x = lanes[i + 1]

                if upward:

                    control_points.append((next_x, top))

                else:

                    control_points.append((next_x, bottom))

            upward = not upward

        # remove duplicated points
        filtered = []

        for p in control_points:

            if len(filtered) == 0 or p != filtered[-1]:

                filtered.append(p)

        # interpolate
        wp_id = 0

        for i in range(len(filtered) - 1):

            p0 = filtered[i]
            p1 = filtered[i + 1]

            segment = self._interpolate_segment(
                p0,
                p1
            )

            if i != 0:
                segment = segment[1:]

            for x, y in segment:

                mission.waypoints.append(

                    Waypoint(
                        id=wp_id,
                        x=x,
                        y=y,
                        z=self.cfg.flight.altitude,
                        speed=self.cfg.flight.speed
                    )

                )

                wp_id += 1

        return mission

    # =====================================================
    # Interpolation
    # =====================================================

    def _interpolate_segment(
        self,
        p0,
        p1
    ):

        spacing = self.cfg.flight.waypoint_spacing

        x0, y0 = p0
        x1, y1 = p1

        distance = math.hypot(
            x1 - x0,
            y1 - y0
        )

        if distance < 1e-6:

            return [p0]

        num = max(
            1,
            math.ceil(distance / spacing)
        )

        pts = []

        for i in range(num + 1):

            t = i / num

            x = x0 + t * (x1 - x0)
            y = y0 + t * (y1 - y0)

            pts.append((x, y))

        return pts