import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python executor.py <path_to_cpp_file>")
    sys.exit(1)

cpp_file = sys.argv[1]

# Compile
compile_process = subprocess.run(
    ["g++", cpp_file, "-o", "prog"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if compile_process.returncode != 0:
    print("Compilation Error:")
    print(compile_process.stderr)
    sys.exit(1)

print("Compilation successful.")

# Run
run_process = subprocess.run(
    ["./prog"],
    stdin=open("testcases/input.txt"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print("Program Output:")
print(run_process.stdout)

if run_process.stderr:
    print("Runtime Error Output:")
    print(run_process.stderr)
