# Project Pause Summary

## Project Status

This project is paused as a bench-validated autonomous search-and-landing UAV prototype

Real flight testing is pending exact compatible threaded-hub or self-locking 1045 propeller replacement

## Completed System Areas

* Raspberry Pi 5 camera setup
* OpenCV ArUco marker detection
* Mounted camera marker tracking
* Pixhawk 6C MAVLink communication over Raspberry Pi UART
* Pixhawk heartbeat, mode, armed-state, and telemetry reading from Raspberry Pi
* Mission state machine for SEARCH, ACQUIRE, TRACK, APPROACH, LAND, and DISARM
* Bounded search pattern logic
* Safety-gated MAVLink command wrapper
* Mounted front-camera offset calibration
* Mounted camera guidance using calibrated drone-center target offset
* Mounted offset mission dry-run from SEARCH to DISARM
* Onboard read-only flight logger
* Sign-mapping read-only logger
* Sign-mapping log analyzer
* Read-only flight checklist

## Final Tested State

The software stack can detect an ArUco marker, compute marker error, apply mounted camera offset calibration, progress through autonomous mission states, generate suggested commands, and block real movement commands through the safety gate

The most complete bench test reached the simulated mission sequence through DISARM

## Hardware Blocker

Real flight testing is blocked by propeller compatibility

The generic 1045 replacement propellers had the correct size category but the wrong mounting style for the current motor shafts

The propeller hubs were too tall for the available threaded shaft length, so the prop nuts could not safely clamp the propellers from above

Improvised mounting methods were rejected for safety

## Required Before Resuming

* Order exact threaded-hub or self-locking 1045 replacement propellers
* Confirm CW and CCW propellers match the known motor spin directions
* Install propellers without adapters or improvised hardware
* Run a short manual read-only flight with Raspberry Pi mounted and flight-powered
* Analyze the sign-mapping log
* Map camera error directions to real drone movement directions
* Test GUIDED mode entry without movement commands
* Test first low-speed safety-gated autonomous centering commands
