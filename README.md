# Online Judge Backend System

A backend system that compiles, executes, and evaluates programming
submissions against test cases, with support for multiple verdicts,
resource limits, output protection, and sequential submission processing.

---

## System Overview

This project implements the core backend of an online judge system,
similar in spirit to platforms like Codeforces or LeetCode.

The system accepts C++ submissions, compiles them, executes them against
predefined test cases, and determines a verdict such as Accepted,
Wrong Answer, Time Limit Exceeded, or Runtime Error.

The design focuses on:
- Correctness of verdicts
- Safety against infinite loops, crashes, and output abuse
- Sequential processing of multiple submissions
- Clear and maintainable backend logic

---

## Architecture

The system is composed of the following components:

- **`executor.py`**
  - Core judging engine
  - Compiles C++ submissions
  - Executes programs with time limits
  - Normalizes and compares outputs
  - Assigns verdicts

- **`queue_manager.py`**
  - Manages a FIFO submission queue
  - Uses a worker thread to process submissions sequentially
  - Prevents concurrent execution of submissions

- **`testcases/`**
  - Contains input test cases

- **`outputs/`**
  - Contains expected outputs for evaluation

- **`tests/`**
  - Contains adversarial submissions used for stress testing
  - Includes infinite loops, huge output spam, syntax errors, etc.

Execution is intentionally sequential to avoid race conditions and
resource contention.

---

## Execution Flow

1. A submission (C++ source file) is added to the submission queue.
2. The worker thread picks the submission from the queue.
3. The submission is compiled using `g++`.
   - Compilation errors immediately terminate evaluation.
4. The compiled program is executed against each test case.
5. During execution:
   - A time limit is enforced using Python subprocess timeouts.
   - Output size is monitored to prevent output flooding.
6. The program output is normalized and compared with the expected output.
7. A verdict is assigned and printed.
8. The worker proceeds to the next submission in the queue.

---

## Verdict Logic

Verdicts are assigned according to the following priority:

1. **Compilation Error (CE)**
   - Submission fails to compile.

2. **Time Limit Exceeded (TLE)**
   - Execution exceeds the configured time limit.

3. **Runtime Error (RE)**
   - Program crashes (segmentation fault, abort)
   - Output size exceeds the configured limit.

4. **Wrong Answer (WA)**
   - Program output does not match the expected output.

5. **Accepted (AC)**
   - Program produces correct output for all test cases within limits.

This strict ordering ensures deterministic and consistent verdicts.

---

## Edge Cases and Hardening

The judge was tested against several adversarial scenarios, including:

- Infinite loops
- Excessively large output (output flooding)
- Invalid or empty C++ files
- Programs producing no output
- Incorrect formatting with extra spaces or newlines

The system is hardened to ensure:
- The judge never hangs
- One bad submission does not block others
- Crashes are handled gracefully
- Output flooding does not exhaust system memory

---

## Limitations

- Memory limits are enforced only on Linux systems using the `resource`
  module. On macOS, memory limiting via `RLIMIT_AS` is not supported,
  so memory-heavy programs may be terminated by the time limit instead.

- The judge operates entirely in user space and does not use kernel-level
  isolation mechanisms such as cgroups or seccomp.

- Only C++ submissions are currently supported.

These limitations are documented intentionally and reflect realistic
constraints of a user-space judge.

---

## Scalability Discussion

The current design processes submissions sequentially using a single
worker thread. This simplifies correctness and avoids resource contention.

To scale this system:
- Multiple worker processes could be introduced.
- Submissions could be distributed using a message broker
  (e.g., Redis or RabbitMQ).
- Resource isolation could be improved using containers or cgroups.
- A persistent database could store submissions and results.

The current implementation intentionally favors correctness,
robustness, and clarity over raw throughput.

---

## How to Run

Run a single submission:

```bash
python executor.py submissions/solution.cpp
