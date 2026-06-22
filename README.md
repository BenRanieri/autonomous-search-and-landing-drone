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
* Closed loop controller simulation
* Simulated error correction over time
* SImulation success detection with boolean flags
* Reusable run_simulation function
* Optional step-by-step simulation output
* Import friendly simulation test structure
* Controller error history recording
* Controller command history recording
* Controller error response plot
* Controller command response plot
* Saved controller response visualizations
* Marker apparent size calculation
* Desired marker size logic
* Marker size tolerance logic
* Closer, maintain, and further distance command testing
* Distance aware guidance connection to marker detection
* Combined guidance command function
* Position and size guidance integration
* Center first guidance priority logic

### In Progress

* Converting combined guidance into numeric movement
* Preparing approach and descent behavior
* Preparing for mission-state logic

### Planned

* Numeric movement from combined guidance
* Approach behavior
* Descent over marker behavior
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

