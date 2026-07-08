from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyArrowPatch

from .models import *


class MissionVisualizer:

    COLORS = [
        "tab:blue",
        "tab:red",
        "tab:green",
        "tab:orange",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray",
    ]

    def __init__(self, planner_cfg: PlannerConfig):

        self.cfg = planner_cfg

    # =====================================================
    # Public
    # =====================================================

    def plot(
        self,
        missions: list[DroneMission],
        show_waypoint=False,
        show_id=False,
        show_arrow=True,
        show_footprint=False,
    ):

        fig, ax = plt.subplots(figsize=(8, 10))

        self._draw_area(ax)
        self._draw_subregions(ax)
        self._draw_paths(
            ax,
            missions,
            show_waypoint,
            show_id,
            show_arrow,
            show_footprint,
        )

        ax.set_aspect("equal")

        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_title("Coverage Planner")

        ax.grid(True)

        plt.tight_layout()
        plt.show()

    # =====================================================
    # Area
    # =====================================================

    def _draw_area(self, ax):

        area = Rectangle(
            (0, 0),
            self.cfg.area.width,
            self.cfg.area.length,
            fill=False,
            linewidth=2,
        )

        ax.add_patch(area)

    def _draw_subregions(self, ax):

        sub_width = (
            self.cfg.area.width
            / self.cfg.drone_num
        )

        for i in range(1, self.cfg.drone_num):

            x = i * sub_width

            ax.plot(
                [x, x],
                [0, self.cfg.area.length],
                "--",
                color="gray",
                linewidth=1,
            )

    # =====================================================
    # Mission
    # =====================================================

    def _draw_paths(
        self,
        ax,
        missions,
        show_waypoint,
        show_id,
        show_arrow,
        show_footprint,
    ):

        fp_w, fp_h = self.cfg.camera.footprint(
            self.cfg.flight.altitude
        )

        for mission in missions:

            color = self.COLORS[
                mission.drone_id % len(self.COLORS)
            ]

            xs = [wp.x for wp in mission.waypoints]
            ys = [wp.y for wp in mission.waypoints]

            ax.plot(
                xs,
                ys,
                color=color,
                linewidth=2,
                label=f"Drone {mission.drone_id}",
            )

            # 起点
            ax.scatter(
                xs[0],
                ys[0],
                s=80,
                marker="o",
                color=color,
            )

            # 终点
            ax.scatter(
                xs[-1],
                ys[-1],
                s=80,
                marker="s",
                color=color,
            )

            # Waypoints
            if show_waypoint:

                ax.scatter(
                    xs,
                    ys,
                    s=10,
                    color=color,
                )

            # Waypoint ID
            if show_id:

                for wp in mission.waypoints:

                    ax.text(
                        wp.x,
                        wp.y,
                        str(wp.id),
                        fontsize=7,
                    )

            # Direction
            if show_arrow:

                step = 1

                for i in range(0, len(mission.waypoints) - step, step):

                    p0 = mission.waypoints[i]
                    p1 = mission.waypoints[i + step]

                    arrow = FancyArrowPatch(
                        (p0.x, p0.y),
                        (p1.x, p1.y),
                        arrowstyle="->",
                        mutation_scale=10,
                        color=color,
                    )

                    ax.add_patch(arrow)

            # Camera footprint
            if show_footprint:

                interval = max(
                    1,
                    len(mission.waypoints) // 20,
                )

                for wp in mission.waypoints[::interval]:

                    rect = Rectangle(
                        (
                            wp.x - fp_w / 2,
                            wp.y - fp_h / 2,
                        ),
                        fp_w,
                        fp_h,
                        fill=False,
                        linewidth=0.5,
                        edgecolor=color,
                        alpha=0.3,
                    )

                    ax.add_patch(rect)

        ax.legend()