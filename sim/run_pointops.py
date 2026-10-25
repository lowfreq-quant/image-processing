"""[DEPRECATED -- superseded, kept for historical reference only]

Compile and run the point-operation golden-model testbench, then verify.

THIS SCRIPT CANNOT RUN ANY MORE: the Verilog testbench it drives (tb_pointops.v)
no longer exists in the tree.  The point-ops verification was redone with cocotb
and passes; use that instead:

    python sim/run_pointops_cocotb.py      # -> sim/test_pointops.py

verify_pointops.py is STILL LIVE -- it holds the four cycle-accurate model
classes (LogModel / EmbossModel / HistogramModel / HistEqModel) that
test_pointops.py imports as its reference.  Do not delete it.

See docs/HANDOFF.md (2026-08-03 and 2026-10-02 entries) for the phase-alignment
history that led to the cocotb rewrite.

Original flow:
  1. gen_pointops_lut.py   -> sim/ip/log_lut.hex   (LOG ROM content)
  2. iverilog tb_pointops  -> pointops.vvp -> sim/pointops_dump.txt
  3. verify_pointops.py    -> cycle-accurate model + functional intent checks

Usage:
    python sim/run_pointops.py
"""

import os
import subprocess
import sys


SIM_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SIM_DIR)
IVERILOG = os.path.join(os.environ.get("IVERILOG_BIN", r"C:\iverilog\bin"), "iverilog.exe")
VVP = os.path.join(os.environ.get("IVERILOG_BIN", r"C:\iverilog\bin"), "vvp.exe")

SOURCES = [
    os.path.join(SIM_DIR, "ip", "behavioral_blk_mem.v"),
    os.path.join(ROOT, "image_processing", "logarithmization", "LOG.v"),
    os.path.join(ROOT, "image_processing", "Emboss", "EMBOSS.v"),
    os.path.join(ROOT, "image_processing", "Histogram", "HISTOGRAM.v"),
    os.path.join(ROOT, "image_processing", "Histogram", "HISTOGRAM_EQ.v"),
    os.path.join(SIM_DIR, "tb_pointops.v"),
]


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
    return result.returncode == 0


def main():
    print("[gen] python gen_pointops_lut.py")
    if not run([sys.executable, os.path.join(SIM_DIR, "gen_pointops_lut.py")],
               SIM_DIR):
        print("ERROR: log LUT generation failed")
        sys.exit(1)

    cmd = [IVERILOG, "-g2012", "-s", "tb_pointops", "-o", "pointops.vvp",
           *SOURCES]
    print(f"[compile] {' '.join(cmd)}")
    if not run(cmd, SIM_DIR):
        print("ERROR: compilation of tb_pointops failed")
        sys.exit(1)

    print(f"[run] {VVP} pointops.vvp")
    if not run([VVP, "pointops.vvp"], SIM_DIR):
        print("ERROR: simulation of tb_pointops failed")
        sys.exit(1)

    print("\n[verify] python verify_pointops.py")
    verifier = os.path.join(SIM_DIR, "verify_pointops.py")
    r = subprocess.run([sys.executable, verifier], cwd=SIM_DIR,
                       capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print(r.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
