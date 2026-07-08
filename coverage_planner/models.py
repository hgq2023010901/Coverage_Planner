from dataclasses import dataclass, field
from typing import List, Optional
import math


# ==========================================================
# Basic Data Structure
# ==========================================================

@dataclass(slots=True)
class Waypoint:
    """Single waypoint."""

    x: float
    y: float
    z: float

    yaw: Optional[float] = None
    speed: float = 5.0

    id: int = 0
    search: bool = True


@dataclass(slots=True)
class DroneMission:
    """Waypoint list of one drone."""

    drone_id: int
    start_x: float
    end_x: float

    waypoints: List[Waypoint] = field(default_factory=list)


# ==========================================================
# Camera Model
# ==========================================================

@dataclass(slots=True)
class CameraConfig:
    """
    Camera parameters.

    HFOV/VFOV are in degree.
    """

    hfov: float          # Horizontal FOV
    vfov: float          # Vertical FOV

    overlap: float = 0.10

    def footprint(self, altitude: float):
        """
        Calculate ground footprint.

        Returns
        -------
        (width, height)
        """

        width = 2.0 * altitude * math.tan(math.radians(self.hfov / 2.0))
        height = 2.0 * altitude * math.tan(math.radians(self.vfov / 2.0))

        return width, height

    def effective_lane_width(self, altitude: float):
        """
        Effective lane spacing after overlap.
        """

        _, height = self.footprint(altitude)

        return height * (1.0 - self.overlap)


# ==========================================================
# Flight Parameters
# ==========================================================

@dataclass(slots=True)
class FlightConfig:

    altitude: float

    speed: float

    waypoint_spacing: float = 20.0


# ==========================================================
# Search Area
# ==========================================================

@dataclass(slots=True)
class SearchArea:

    width: float      # Ax

    length: float     # Ay


# ==========================================================
# Planner Config
# ==========================================================

@dataclass(slots=True)
class PlannerConfig:

    area: SearchArea

    camera: CameraConfig

    flight: FlightConfig

    drone_num: int

    keep_outside: bool = False