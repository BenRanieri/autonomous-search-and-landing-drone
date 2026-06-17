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
* Controller test script
* Deadband boundary testing
* Command limit boundary testing
* Contoller behavior classification

### In Progress

* Controller testing
* Preparing for drone correction simulation
* Simulated marker movement

### Planned

* Simulate drone correction behavior
* Visualize controller response
* Test proportional controller over time
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

