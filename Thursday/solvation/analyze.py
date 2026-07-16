import os
import subprocess
import itertools
import glob

import numpy as np
import pandas as pd

import alchemlyb
from alchemlyb.parsing.gmx import extract_dHdl, extract_u_nk
from alchemlyb.estimators import TI, BAR, MBAR
from alchemlyb.preprocessing.subsampling import decorrelate_dhdl, decorrelate_u_nk
from alchemlyb.postprocessors.units import to_kcalmol
from alchemlyb.visualisation import plot_mbar_overlap_matrix, plot_ti_dhdl, plot_dF_state

import matplotlib.pyplot as plt

TEMPERATURE = 300.0  # Kelvin

output_dir = "larger_outputs"

# Set to match which production method you ran: True = expanded ensemble, False = fixed-lambda.

def load_leg(leg_dir, temperature: float = TEMPERATURE):

    """Parse a leg's production output into combined alchemlyb dHdl/u_nk
    formats and discard the burn-in/calibration period.

    """

    files = glob.glob(f"{leg_dir}/ethanol.*.dhdl.xvg")
    xvgs = sorted(files,
        key=lambda x: int(x.split(".")[1])  # numeric lambda order
    )
    if not xvgs:
        raise FileNotFoundError(
            f"No {leg_dir}/ethanol.*.dhdl.xvg files found -- "
            f"has the fixed-lambda production run finished? "
        )
    print(f"  {leg_dir}: {len(xvgs)} fixed-lambda state xvg files")
    dHdl = alchemlyb.concat([extract_dHdl(str(p), T=temperature) for p in xvgs])
    u_nk = alchemlyb.concat([extract_u_nk(str(p), T=temperature) for p in xvgs])

    # Decorrelate EACH state's own timeseries, THEN concatenate.
    dHdl_list, u_nk_list = [], []
    for p in xvgs:
        d = extract_dHdl(str(p), T=temperature)
        u = extract_u_nk(str(p), T=temperature)
        dHdl_list.append(decorrelate_dhdl(d, remove_burnin=True))
        u_nk_list.append(decorrelate_u_nk(u, remove_burnin=True))
    dHdl = alchemlyb.concat(dHdl_list)
    u_nk = alchemlyb.concat(u_nk_list)

    print(f"  {leg_dir}: {len(dHdl)} decorrelated dhdl samples retained "
          f"(post-burn-in, post-subsampling)")
    print(f"  {leg_dir}: {u_nk.shape[0]} decorrelated u_nk samples retained "
          f"(post-burn-in, post-subsampling)")
    return dHdl, u_nk


def estimate_leg(leg_dir, temperature: float = TEMPERATURE):
    """Estimate the free energy of one leg (solvent or complex) via TI and
    MBAR, and produce the standard diagnostic plots (MBAR overlap matrix,
    TI dH/dlambda curve).

    Returns:
        results: dict of {estimator_name: (dG_kcal, err_kcal)}
        (ti, mbar): fitted estimator objects, for use in plot_dF_state
    """

    dHdl, u_nk = load_leg(leg_dir, temperature=temperature)

    ti = TI().fit(dHdl)
    mbar = MBAR().fit(u_nk)
    bar = BAR().fit(u_nk)
    
    results = {}
    for name, est in [("TI", ti), ("MBAR", mbar), ("BAR",bar)]:
        dG = to_kcalmol(est.delta_f_, T=temperature).iloc[0, -1]
        err = to_kcalmol(est.d_delta_f_, T=temperature).iloc[0, -1]
        results[name] = (dG, err)
        print(f" {name}: {dG:.2f} ± {err:.2f} kcal/mol")

    # MBAR overlap matrix
    ax = plot_mbar_overlap_matrix(mbar.overlap_matrix)
    ax.set_title("MBAR overlap matrix")
    plt.savefig(f"{leg_dir}/overlap_matrix.png", dpi=150, bbox_inches="tight")
    plt.show()

    # TI dH/dlambda curve
    ax = plot_ti_dhdl([ti], labels=["(Coul)", "(VDW)"])
    plt.savefig(f"{leg_dir}/ti_dhdl.png", dpi=150, bbox_inches="tight")
    plt.show()

    return results, (ti, mbar, bar)

results, estimators = estimate_leg(output_dir)

