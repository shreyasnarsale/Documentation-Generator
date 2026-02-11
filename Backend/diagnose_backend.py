import sys
import traceback
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

output_file = "diagnosis.txt"

try:
    print("Attempting to import main...")
    import main
    print("Successfully imported main.")
    with open(output_file, "w") as f:
        f.write("SUCCESS: Imported main module without errors.\n")

except Exception as e:
    print(f"Failed to import main: {e}")
    with open(output_file, "w") as f:
        f.write(f"ERROR: {type(e).__name__}: {str(e)}\n")
        f.write(traceback.format_exc())
