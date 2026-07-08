from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from .models import *


class CoverageAnalyzer:

    def __init__(
        self,
        config: PlannerConfig,
        resolution: float = 0.5,
    ):
        """
        resolution:
            Grid resolution (m/cell)
        """

        self.cfg = config
        self.resolution = resolution

        self.width = int(
            np.ceil(
                config.area.width / resolution
            )
        )

        self.height = int(
            np.ceil(
                config.area.length / resolution
            )
        )

    # =====================================================
    # Public
    # =====================================================

    def analyze(
        self,
        missions: list[DroneMission],
    ):

        coverage = np.zeros(
            (self.height, self.width),
            dtype=np.uint16,
        )

        fp_w, fp_h = self.cfg.camera.footprint(
            self.cfg.flight.altitude
        )

        for mission in missions:

            for wp in mission.waypoints:

                self._paint(
                    coverage,
                    wp.x,
                    wp.y,
                    fp_w,
                    fp_h,
                )

        return coverage

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(
        self,
        coverage,
        missions,
    ):

        total = coverage.size

        covered = np.sum(coverage >= 1)

        overlap = np.sum(coverage >= 2)

        coverage_ratio = covered / total

        overlap_ratio = overlap / total

        total_distance = 0.0

        total_wp = 0

        for mission in missions:

            total_wp += len(mission.waypoints)

            for i in range(len(mission.waypoints)-1):

                p0 = mission.waypoints[i]
                p1 = mission.waypoints[i+1]

                total_distance += np.hypot(
                    p1.x-p0.x,
                    p1.y-p0.y,
                )

        est_time = (
            total_distance /
            self.cfg.flight.speed
        )

        print()

        print("="*50)

        print(f"Coverage Ratio : {coverage_ratio*100:.2f}%")

        print(f"Overlap Ratio  : {overlap_ratio*100:.2f}%")

        print(f"Missed Area    : {(1-coverage_ratio)*100:.2f}%")

        print(f"Waypoints      : {total_wp}")

        print(f"Distance       : {total_distance:.1f} m")

        print(f"Flight Time    : {est_time:.1f} s")

        print("="*50)

    # =====================================================
    # Plot
    # =====================================================

    def plot(
        self,
        coverage,
    ):

        plt.figure(figsize=(8,10))

        plt.imshow(
            coverage,
            origin="lower",
            interpolation="nearest",
            extent=[
                0,
                self.cfg.area.width,
                0,
                self.cfg.area.length,
            ]
        )

        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.title("Coverage Heatmap")

        plt.colorbar(
            label="Coverage Count"
        )

        plt.tight_layout()
        plt.show()

    # =====================================================
    # Paint
    # =====================================================

    def _paint(
        self,
        grid,
        x,
        y,
        fp_w,
        fp_h,
    ):

        xmin = max(
            0,
            int((x-fp_w/2)/self.resolution),
        )

        xmax = min(
            self.width-1,
            int((x+fp_w/2)/self.resolution),
        )

        ymin = max(
            0,
            int((y-fp_h/2)/self.resolution),
        )

        ymax = min(
            self.height-1,
            int((y+fp_h/2)/self.resolution),
        )

        grid[
            ymin:ymax+1,
            xmin:xmax+1
        ] += 1