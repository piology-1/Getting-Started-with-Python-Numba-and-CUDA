# Getting Started with Python, Numba, and CUDA

A comprehensive guide and starter kit for high-performance GPU computing using Python and Numba on Windows 11. This repository documents the setup process and provides code examples to test a cuda installtion with numba and python.

## Overview

This project serves as a "First Steps" guide for leveraging NVIDIA GPUs using the Numba JIT compiler. It includes detailed setup notes for Windows 11 (addressing common version conflicts) and a first basic parallel vector addition kernel.

## Project Structure

```text
.
├── docs/
│   └── installation.md      # Windows 11 setup & troubleshooting notes
├── examples/
│   ├── test_cuda.py         # Hardware & driver diagnostic tool
│   └── vector_addition.py   # GPU-accelerated parallel addition kernel
├── .gitignore
├── .python-version
├── pyproject.toml           # Project dependencies (Numba, NumPy)
├── uv.lock
└── README.md
```

## Prerequisites

- **OS:** Windows 11
- **Hardware:** NVIDIA GPU (e.g., GTX 1660 Ti)
- **Tools:** - [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (v12.8 recommended)
  - [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)

## Setup & Installation

This project uses `uv`.

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/piology-1/Getting-Started-with-Python-Numba-and-CUDA.git](https://github.com/piology-1/Getting-Started-with-Python-Numba-and-CUDA.git) numba-cuda-guide
   cd numba-cuda-guide
   ```

2. **Sync the environment:**
   ```bash
   uv sync
   ```

## Running the Examples

### 1. Verify CUDA Connection

Check if your GPU is detected and the CUDA libraries are properly linked:

```bash
uv run .\examples\test_cuda.py
```

### 2. Run GPU Vector Addition

Perform a parallel calculation on 10 million elements to verify functional GPU acceleration:

```bash
uv run .\examples\vector_addition.py
```

## Documentation

For a detailed log of the installation process, version downgrades (CUDA 13.x to 12.8), and environment variable configuration, see the [log](/docs/installation.md)
