###############################################################################
# Makefile for cocotb + Icarus Verilog simulation of RGB2YUV
###############################################################################

TOPLEVEL_LANG = verilog

# Iverilog installation path
export PATH := $(PATH):/c/iverilog/bin

# Top-level Verilog module name
TOPLEVEL = RGB2YUV

# cocotb Python test module
MODULE = test_rgb2yuv

# Verilog source files
VERILOG_SOURCES = $(abspath ../image_processing/RGB_to_YUV/RGB2YUV.v)

# Tell iverilog to compile with the right timescale
COMPILE_ARGS = -g2012

# cocotb library path - let it find it
COCOTB?=

# Include cocotb's rules
include $(shell python -c "import cocotb; print(cocotb.__file__)" 2>/dev/null | sed 's/__init__\.py//')makefiles/Makefile.sim

# Default target
all: sim

# Run simulation
sim:
	$(MAKE) -C . sim

# Clean
clean::
	rm -rf sim_build/
	rm -f *.vcd *.fst *.dump *.log results.xml
