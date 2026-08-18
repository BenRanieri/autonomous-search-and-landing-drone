# Resume and Portfolio Summary

## Resume Project Title

Autonomous Search-and-Landing UAV Prototype

## Resume Technology Line

Python, OpenCV, ArUco, Raspberry Pi 5, Pixhawk 6C, MAVLink, ArduPilot, Git

## Resume Bullets

* Built a Raspberry Pi-based computer vision pipeline using OpenCV and ArUco markers for UAV landing target detection
* Integrated Raspberry Pi 5 with Pixhawk 6C over UART/MAVLink to read vehicle mode, armed state, telemetry, and onboard camera target data
* Designed a mission state machine for SEARCH, ACQUIRE, TRACK, APPROACH, LAND, and DISARM phases
* Implemented a safety-gated MAVLink command wrapper to block unsafe movement commands unless real-command, flight-test, pilot-readiness, mode, arming, and command-limit checks pass
* Calibrated an offset-mounted onboard camera and validated drone-center target tracking through a mounted bench dry-run
* Created onboard read-only flight logging tools for marker position, marker size, vehicle state, and suggested guidance commands

## Short Resume Version

Autonomous Search-and-Landing UAV Prototype | Python, OpenCV, Raspberry Pi, Pixhawk, MAVLink

* Integrated Raspberry Pi vision with Pixhawk telemetry over MAVLink for ArUco-based landing target detection
* Developed search, target acquisition, tracking, approach, and landing state-machine logic with safety-gated command handling
* Calibrated an offset-mounted onboard camera and validated the full guidance sequence in bench dry-run testing

## Honest Status Line

Bench-validated autonomy and perception stack; flight testing paused pending compatible threaded-hub 1045 propeller replacement

## Interview Explanation

The software and bench validation are complete. I integrated the Raspberry Pi, Pixhawk, camera, MAVLink connection, safety gate, search logic, mounted camera calibration, and read-only logging tools. Real flight testing was paused because the replacement propellers I received were the wrong mounting style for the Holybro motor shafts, and I chose not to fly with unsafe improvised propeller hardware.
