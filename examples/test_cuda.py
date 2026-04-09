from numba import cuda
import sys


def run_diagnostics():
    """
    Performs a diagnostic check of the local Python environment
    and its connection to NVIDIA CUDA drivers/hardware.
    """

    print("-" * 30)
    print("PYTHON & CUDA DIAGNOSTICS")
    print("-" * 30)

    # 1. System Info: Identifies the Python interpreter version
    print(f"Python Version: {sys.version.split()[0]}")

    # 2. Library Verification:
    # This specifically checks if Numba can find the required NVIDIA DLLs
    # (like nvvm.dll or cudart.dll) on your Windows PATH.
    print("\nChecking CUDA Libraries:")
    try:
        cuda.cudadrv.libs.test()
        print("[✅] CUDA Libraries: Functional")
    except Exception as e:
        print(f"[❌] CUDA Libraries: Failed\nDetails: {e}")

    # 3. Availability Check:
    # Returns True if a CUDA-enabled GPU and the correct drivers are found.
    available = cuda.is_available()
    print(f"\nCUDA Available: {available}")

    if available:
        # 4. Hardware Enumeration:
        # Loops through all detected NVIDIA GPUs to print technical specs.
        print("\nDetected GPU(s):")
        try:
            for device in cuda.list_devices():

                # Using 'with device' ensures the context is correctly initialized
                with device:
                    # device.name is returned as bytes, so we decode it to a string
                    print(f"  > {device.name.decode('utf-8')}")

        except Exception as e:
            print(f"Could not retrieve device details: {e}")
    else:
        print("\n[!] No NVIDIA GPU detected. Check your drivers and 'nvcc --version'.")

    print("-" * 30)


if __name__ == "__main__":
    run_diagnostics()
