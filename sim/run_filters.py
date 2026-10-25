"""Run the combined filters testbench via cocotb runner (no Makefile needed)."""
import os
import sys
from pathlib import Path
from cocotb_tools.runner import get_runner

# cocotb 2.x needs the iverilog binary on PATH (or IVERILOG_BIN env)
os.environ["PATH"] = r"C:\iverilog\bin;" + os.environ.get("PATH", "")
os.environ.setdefault("SIM", "icarus")

ROOT = Path(__file__).resolve().parent
PRJ = ROOT.parent

verilog_sources = [
    str(PRJ / "sim/ip/behavioral_fifo.v"),
    str(PRJ / "sim/ip/behavioral_cordic.v"),
    str(PRJ / "sim/ip/ip_wrappers.v"),
    str(PRJ / "image_processing/Matrix_generator/matrix_generator.v"),
    str(PRJ / "image_processing/Gaussian_filter/gaussian_filter.v"),
    str(PRJ / "image_processing/Sobel_detection/sobel.v"),
    str(PRJ / "image_processing/Median_filter/median_filter.v"),
    str(PRJ / "sim/tb_filters.v"),
]  

runner = get_runner("icarus")
runner.build(
    verilog_sources=verilog_sources,
    hdl_toplevel="tb_filters",
    build_dir=str(ROOT / "build_filters"),
    always=True,
    build_args=["-g2012"],
)

runner.test(
    test_module="test_filters",
    hdl_toplevel="tb_filters",
    test_dir=str(ROOT),
)
