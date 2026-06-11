# Autonomous Search and Landing UAV

A computer-vision-guided autonomous UAV capable of autonomous takeoff, search, target acquisition, target tracking, and precision landing.

This project combines robotics, aerospace engineering, computer vision, guidance and control, simulation, and hardware integration to develop a complete autonomous aerial mission system.



## Current Status

### Completed

* Development environment setup
* GitHub workflow
* OpenCV integration
* ArUco marker generation
* ArUco marker detection
* Marker corner extraction

### In Progress

* Marker center estimation
* Position error calculation

### Planned

* Autonomous takeoff
* Search behavior
* Target acquisition
* Target tracking
* Precision landing
* Hardware integration



## System Architecture

Camera
↓
Computer Vision
↓
Target Detection
↓
Position Estimation
↓
Guidance System
↓
Flight Controller
↓
UAV Motion

Mission States:

TAKEOFF
↓
SEARCH
↓
ACQUIRE
↓
TRACK
↓
APPROACH
↓
LAND
↓
DISARM

