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
* Numeric elevation command function
* Approach command tuning value
* Final numeric movement command function
* Final movement output connected to marker detection
* Final movement simulation
* Finalized movement command loop
* Center, distance-adjust, and maintain behavior sequence
* Reusable final movement simulation function
* Final movement simulation summaries
* Final movement testing for closer, further, maintain, and large error cases
* Final movement simulation history rtacking
* Final movement position error plot
* Final movement marker size plot
* Final movement command plot

### In Progress

* Cleaning up final movement simulation and plotting code
* Preparing final movement results for documentation
* Preparing for mission-state logic

### Planned

* Plot helper functions
* Explain final movement results
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

