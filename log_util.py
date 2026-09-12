# log_util.py
# A homemade logger.
# Written in 2013; modernised 2024. The logging module is the right long-term replacement.

import time

LOG_LINES: list[str] = []       # module-level buffer; flushed to disk by flush_log()


def log(message: str) -> None:
    """Append a timestamped message to the in-memory log buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to path (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
