from queue import Queue
import threading
import subprocess

submission_queue = Queue()

def worker():
    while True:
        cpp_file = submission_queue.get()
        print(f"[Worker] Processing submission: {cpp_file}")

        subprocess.run(
            ["python", "executor.py", cpp_file]
        )

        submission_queue.task_done()

worker_thread = threading.Thread(
    target=worker,
    daemon=True
)
worker_thread.start()

if __name__ == "__main__":
    submissions = [
    "submissions/solution_ac.cpp",
    "submissions/solution_wa.cpp",
    "submissions/solution_tle.cpp",
    "submissions/solution_re.cpp",
    "submissions/solution_mem.cpp",
    "submissions/solution_ce.cpp",
]


    for sub in submissions:
        print(f"[Main] Adding {sub} to queue")
        submission_queue.put(sub)

    submission_queue.join()
    print("All submissions processed.")
