import subprocess
import sys
import os
import platform

# ----------------------------
# Limits
# ----------------------------
TIME_LIMIT = 2  # seconds
MEMORY_LIMIT = 256 * 1024 * 1024  # 256 MB
MAX_OUTPUT_SIZE = 1_000_000  # 1 MB output cap

IS_LINUX = platform.system() == "Linux"

def limit_resources():
    # Memory limiting only supported on Linux
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))

# ----------------------------
# Step 1: Read C++ file path
# ----------------------------
if len(sys.argv) < 2:
    print("Usage: python executor.py <path_to_cpp_file>")
    sys.exit(1)

cpp_file = sys.argv[1]

# ----------------------------
# Step 2: Compile
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
            text=True,
            timeout=TIME_LIMIT,
            preexec_fn=limit_resources if IS_LINUX else None
        )

    # ----------------------------
    # Time Limit Exceeded
    # ----------------------------
    except subprocess.TimeoutExpired:
        verdict = "TLE"
        print(f"Time Limit Exceeded on {input_file}")
        break

    # ----------------------------
    # Runtime Error (crash / signal)
    # ----------------------------
    if run_process.returncode != 0:
        verdict = "RE"
        print(f"Runtime Error on {input_file}")
        break

    # ----------------------------
    # Output Size Limit (Huge Output Spam)
    # ----------------------------
    raw_output = run_process.stdout

    if len(raw_output) > MAX_OUTPUT_SIZE:
        verdict = "RE"
        print(f"Output Limit Exceeded on {input_file}")
        break

    # ----------------------------
    # Output normalization
    # ----------------------------
    user_output = raw_output.strip()

    with open(expected_path) as f:
        expected_output = f.read().strip()

    # ----------------------------
    # Wrong Answer
    # ----------------------------
    if user_output != expected_output:
        verdict = "WA"
        print(f"Wrong Answer on {input_file}")
        break

# ----------------------------
# Step 5: Print verdict
# ----------------------------
print("Final Verdict:", verdict)
