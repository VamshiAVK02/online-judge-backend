import subprocess
import sys
import os

# ----------------------------
# Step 1: Read C++ file path
# ----------------------------
if len(sys.argv) < 2:
    print("Usage: python executor.py <path_to_cpp_file>")
    sys.exit(1)

cpp_file = sys.argv[1]

# ----------------------------
# Step 2: Compile the code
# ----------------------------
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

# ----------------------------
# Step 3: Load test cases
# ----------------------------
input_dir = "testcases"
output_dir = "outputs"

input_files = sorted(os.listdir(input_dir))

# ----------------------------
# Step 4: Run test cases
# ----------------------------
verdict = "AC"

for input_file in input_files:
    input_path = os.path.join(input_dir, input_file)

    expected_file = "expected" + input_file.replace("input", "")
    expected_path = os.path.join(output_dir, expected_file)

    try:
        run_process = subprocess.run(
            ["./prog"],
            stdin=open(input_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception:
        verdict = "RE"
        print(f"Runtime Error on {input_file}")
        break

    # ----------------------------
    # Runtime Error check
    # ----------------------------
    if run_process.returncode != 0:
        verdict = "RE"
        print(f"Runtime Error on {input_file}")
        break

    # ----------------------------
    # Output normalization
    # ----------------------------
    user_output = run_process.stdout.strip()

    with open(expected_path) as f:
        expected_output = f.read().strip()

    # ----------------------------
    # Wrong Answer check
    # ----------------------------
    if user_output != expected_output:
        verdict = "WA"
        print(f"Wrong Answer on {input_file}")
        break

# ----------------------------
# Step 5: Print verdict
# ----------------------------
print("Final Verdict:", verdict)
