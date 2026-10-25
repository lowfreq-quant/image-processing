"""Run test_isp_chain.py via the cocotb runner.

Compiles the full ISP_TOP data path (RGB2YUV + LOG + gaussian + median +
sobel + canny, no SDRAM) with the behavioral IP models and runs the
cycle-accurate chain verification.

Usage:
    python sim/run_isp_chain.py
"""

import os
from pathlib import Path
from cocotb_tools.runner import get_runner

import gen_pointops_lut


os.environ["PATH"] = r"C:\iverilog\bin;" + os.environ.get("PATH", "")
os.environ.setdefault("SIM", "icarus")

ROOT = Path(__file__).resolve().parent
PRJ = ROOT.parent

gen_pointops_lut.main()

verilog_sources = [
    str(ROOT / "ip" / "behavioral_fifo.v"),
    str(ROOT / "ip" / "behavioral_cordic.v"),
    str(ROOT / "ip" / "ip_wrappers.v"),
    str(ROOT / "ip" / "behavioral_blk_mem.v"),
    str(PRJ / "image_processing" / "Matrix_generator" / "matrix_generator.v"),
    str(PRJ / "image_processing" / "RGB_to_YUV" / "RGB2YUV.v"),
    str(PRJ / "image_processing" / "logarithmization" / "LOG.v"),
    str(PRJ / "image_processing" / "Gaussian_filter" / "gaussian_filter.v"),
    str(PRJ / "image_processing" / "Median_filter" / "median_filter.v"),
    str(PRJ / "image_processing" / "Sobel_detection" / "sobel.v"),
    str(PRJ / "image_processing" / "Canny_detection" / "canny.v"),
    str(ROOT / "tb_isp_chain.v"),
]

runner = get_runner("icarus")
runner.build(
    verilog_sources=verilog_sources,
    hdl_toplevel="tb_isp_chain",
    build_dir=str(ROOT / "build_isp_chain"),
    always=True,
    build_args=["-g2012"],
)
runner.test(
    test_module="test_isp_chain",
    hdl_toplevel="tb_isp_chain",
    test_dir=str(ROOT),
)