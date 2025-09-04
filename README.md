# SWMM–CFD Coupling Manual

Thanks to the useful **[foamlib](https://github.com/gerlero/foamlib)** package, this project demonstrates a simplified coupling between **SWMM** and **CFD (OpenFOAM)**.  
Although slower than the original implementation, this version is **clear, simple, and easy to use**.  
The old version is archived under `old_files/` for reference.

---

## Features

- **Simplicity**: Straightforward code with a clear main loop.  
- **Convenience**: Minimal configuration needed to start coupled runs.  
- **Traceability**: Old code archived in `old_files/`.  

---

## Requirements

- [OpenFOAM](https://openfoam.org/) installed with environment variable `FOAM_TUTORIALS` set.  
- [SWMM](https://www.epa.gov/water-research/storm-water-management-model-swmm) input file available (e.g., `SWMM/swmm.inp`).  
- Python packages:
  - `foamlib`
  - `pyswmm`
  - `python-dateutil`

---

## Quick Start

1. **Set up environment**
   ```bash
   export FOAM_TUTORIALS=/path/to/OpenFOAM/tutorials
   pip install foamlib pyswmm python-dateutil
   ```

2. **Run the coupling script**
   ```bash
   python swmm_cfd.py
   ```

3. **Workflow**
   - Clone the `pitzDaily` tutorial from `$FOAM_TUTORIALS`.  
   - Run SWMM simulation step by step.  
   - Within `openfoam_range`, OpenFOAM is triggered for short runs.  
   - Inflow from SWMM node (e.g., `J4`) is mapped to the OpenFOAM inlet via `flowRateInletVelocity`.  
   - Log files are cleaned automatically after each OpenFOAM run.  



---

## Example Code Snippet

```python
inflow = Nodes(sim_swmm)["J4"].total_outflow
boundaryDict = {
    "U": {
        "inlet": {
            "type": "flowRateInletVelocity",
            "volumetricFlowRate": inflow,
        }
    }
}
step_openfoam(sim_swmm, my_pitz, openfoam_range, step, boundaryDict)
```

---


## Notes

- Adjust `openfoam_range` in the script to control when OpenFOAM runs.  
- Change SWMM node ID (currently `"J4"`) to match your model.  
- For inflows, the `flowRateInletVelocity` boundary condition is recommended.  
- `my_pitz.clean()` ensures OpenFOAM case is reset after simulation.
