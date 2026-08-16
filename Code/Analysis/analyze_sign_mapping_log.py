import csv
import sys
from pathlib import Path
from statistics import mean


project_root = Path(__file__).resolve().parents[2]
logs_dir = project_root / "logs"


def find_latest_log():
    log_files = list(logs_dir.glob("sign_mapping_readonly_*.csv"))

    if len(log_files) == 0:
        return None

    return max(log_files, key=lambda path: path.stat().st_mtime)


def parse_float(value):
    if value is None:
        return None

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def average(values):
    clean_values = [value for value in values if value is not None]

    if len(clean_values) == 0:
        return None

    return mean(clean_values)


def rounded(value):
    if value is None:
        return "None"

    return round(value, 3)


def load_rows(log_path):
    with open(log_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def split_into_segments(rows):
    segments = []
    current_segment = None

    for row in rows:
        phase = row.get("phase", "UNKNOWN")
        instruction = row.get("instruction", "")

        if (
            current_segment is None
            or current_segment["phase"] != phase
            or current_segment["instruction"] != instruction
        ):
            current_segment = {
                "phase": phase,
                "instruction": instruction,
                "rows": [],
            }

            segments.append(current_segment)

        current_segment["rows"].append(row)

    return segments


def summarize_segment(segment):
    rows = segment["rows"]

    detected_rows = [
        row for row in rows
        if row.get("marker_detected") == "True"
    ]

    detection_rate = len(detected_rows) / len(rows) if len(rows) > 0 else 0

    return {
        "phase": segment["phase"],
        "instruction": segment["instruction"],
        "rows": len(rows),
        "detections": len(detected_rows),
        "detection_rate": detection_rate,
        "avg_alt": average([parse_float(row.get("relative_alt_m")) for row in rows]),
        "avg_error_x": average([parse_float(row.get("error_x")) for row in detected_rows]),
        "avg_error_y": average([parse_float(row.get("error_y")) for row in detected_rows]),
        "avg_adjusted_x": average([parse_float(row.get("adjusted_error_x")) for row in detected_rows]),
        "avg_adjusted_y": average([parse_float(row.get("adjusted_error_y")) for row in detected_rows]),
        "avg_marker_size": average([parse_float(row.get("marker_size")) for row in detected_rows]),
    }


def print_segment_summary(summaries):
    print()
    print("Segment summary")
    print("-" * 120)

    for index, summary in enumerate(summaries):
        print(
            "segment:",
            index,
            "phase:",
            summary["phase"],
            "rows:",
            summary["rows"],
            "detections:",
            summary["detections"],
            "detect_rate:",
            round(summary["detection_rate"], 2),
            "avg_alt:",
            rounded(summary["avg_alt"]),
            "avg_error_x:",
            rounded(summary["avg_error_x"]),
            "avg_error_y:",
            rounded(summary["avg_error_y"]),
            "avg_adjusted_x:",
            rounded(summary["avg_adjusted_x"]),
            "avg_adjusted_y:",
            rounded(summary["avg_adjusted_y"]),
            "avg_marker_size:",
            rounded(summary["avg_marker_size"]),
        )


def print_movement_comparison(summaries):
    print()
    print("Movement comparison against previous CENTER_HOVER segment")
    print("-" * 120)

    previous_center = None

    for summary in summaries:
        phase = summary["phase"]

        if phase == "CENTER_HOVER":
            previous_center = summary
            continue

        if not phase.startswith("MOVE_"):
            continue

        if previous_center is None:
            print(phase, "has no previous CENTER_HOVER segment")
            continue

        delta_adjusted_x = None
        delta_adjusted_y = None

        if (
            summary["avg_adjusted_x"] is not None
            and previous_center["avg_adjusted_x"] is not None
        ):
            delta_adjusted_x = summary["avg_adjusted_x"] - previous_center["avg_adjusted_x"]

        if (
            summary["avg_adjusted_y"] is not None
            and previous_center["avg_adjusted_y"] is not None
        ):
            delta_adjusted_y = summary["avg_adjusted_y"] - previous_center["avg_adjusted_y"]

        print(
            "phase:",
            phase,
            "delta_adjusted_x:",
            rounded(delta_adjusted_x),
            "delta_adjusted_y:",
            rounded(delta_adjusted_y),
            "move_avg_x:",
            rounded(summary["avg_adjusted_x"]),
            "move_avg_y:",
            rounded(summary["avg_adjusted_y"]),
            "previous_center_x:",
            rounded(previous_center["avg_adjusted_x"]),
            "previous_center_y:",
            rounded(previous_center["avg_adjusted_y"]),
        )


def main():
    if len(sys.argv) >= 2:
        log_path = Path(sys.argv[1])
    else:
        log_path = find_latest_log()

    if log_path is None:
        print("No sign_mapping_readonly CSV logs found")
        raise SystemExit

    if not log_path.exists():
        print("Log file does not exist:", log_path)
        raise SystemExit

    rows = load_rows(log_path)

    if len(rows) == 0:
        print("Log file has no rows:", log_path)
        raise SystemExit

    segments = split_into_segments(rows)
    summaries = [summarize_segment(segment) for segment in segments]

    print("Analyzing sign-mapping log")
    print("Log path:", log_path)
    print("Rows:", len(rows))
    print("Segments:", len(segments))

    print_segment_summary(summaries)
    print_movement_comparison(summaries)

    print()
    print("Analysis complete")


if __name__ == "__main__":
    main()
