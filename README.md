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
* Marker center estimation
* Position error calculation
* Detection visualization
* Guidance logic
* Tolerance logic
* Vision to guidance connection
* Reusable marker detection function
* Marker ID extraction
* Image load error handling
* Marker detection error handling
* Optional marker visualization output
* Proportional guidance command function
* Proportional gain using kp
* Maximum command limiting using maxCommand

### In Progress

* Controller testing
* Modular vision to guidance connection
* Preparing for simulated marker movement

### Planned

* Test proportional control across multiple marker positions
* Simulate drone correction behavior
* Visualize controller response
* Use marker apparent size for distance-aware control
* Mission-state logic
* Autonomous takeoff
* Search behavior
* Target acquisition
* Target tracking
* Controlled descent over marker
* Precision landing
* Hardware selection
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

