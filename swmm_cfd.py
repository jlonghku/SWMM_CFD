import os
import shutil
from pathlib import Path
from datetime import datetime
from dateutil import parser

from foamlib import FoamCase
from pyswmm import Simulation, Nodes


def step_openfoam(sim_swmm, sim_openfoam, date_range, step, boundaryDict):
    """Advance OpenFOAM one step if current SWMM time falls in date_range."""
    date_range = [parser.parse(s) if not isinstance(s, datetime) else s for s in date_range]

    if date_range[0] < sim_swmm.current_time <= date_range[1]:
        latest = sim_openfoam[-1]

        # Update boundary conditions
        if boundaryDict:
            for field, v in boundaryDict.items():
                for bnd_name, v1 in v.items():
                    latest[field].boundary_field[bnd_name].update(v1)

        # Update controlDict for next short run
        sim_openfoam.control_dict.update({
            "startFrom": "latestTime",
            "endTime": latest.time + step
        })

        # Clean logs to keep outputs tidy
        for f in sim_openfoam.path.glob("log.*"):
            f.unlink(missing_ok=True)

        sim_openfoam.run()
        print(f"OpenFOAM step finished at {sim_swmm.current_time}")


if __name__ == "__main__":
    # --- Initialize OpenFOAM case ---
    my_pitz = FoamCase("myPitz")
    my_pitz.control_dict.update({"deltaT": 0.01, "writeInterval": 0.1})

    # Time window during which OpenFOAM is triggered
    openfoam_range = ["2017-11-01 00:00:02", "2017-11-01 00:00:05"]

    # --- Main loop: SWMM ↔ OpenFOAM coupling ---
    boundaryDict = None
    try:
        with Simulation(r"SWMM/swmm.inp") as sim_swmm:
            prev_time = sim_swmm.start_time

            for _ in sim_swmm:
                step = (sim_swmm.current_time - prev_time).seconds
                prev_time = sim_swmm.current_time

                # Push one OF step if within the coupling window
                step_openfoam(sim_swmm, my_pitz, openfoam_range, step, boundaryDict)

                # Pull inflow from SWMM (example: node J4) and map to OF inlet
                inflow = Nodes(sim_swmm)["J4"].total_outflow
                boundaryDict = {
                    "U": {
                        "inlet": {
                            "type": "flowRateInletVelocity",
                            "volumetricFlowRate": inflow,
                        }
                    }
                }
    finally:
        # --- Clean OpenFOAM case ---
        my_pitz.clean()
