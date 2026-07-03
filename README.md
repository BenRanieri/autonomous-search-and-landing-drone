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
* Controller behavior classification
* Closed loop controller simulation
* Simulated error correction over time
* Simulation success detection with boolean flags
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
* Final movement simulation history tracking
* Final movement position error plot
* Final movement marker size plot
* Final movement command plot
* Reusable final movement plotting helper
* Refactored final movement plotting code
* Final movement simulation README documentation
* Final movement plot explanations
* Final movement command history summary
* Command mode counting for final movement simulation
* Readable command summary output
* Harder final movement simulation test cases
* Labeled final movement test cases
* Step-count output for final movement tests
* Final movement stress-test evaluation
* Command summaries for final movement test cases
* Normal and stress labels for final movement tests
* Command-mode comparison across starting conditions
* Cleaner final movement test output

### In Progress

* Controller parameter tuning
* Preparing physical command interface
* Preparing for mission state logic 

### Planned

* Tune controller parameters
* Choose default controller values
* Physical command interface
* Mission-state logic
* Simulated autonomous takeoff
* Autonomous search behavior
* Target acquisition
* Target tracking
* Approach behavior
* Controlled descent over marker
* Precision landing
* Early hardware path comparison
* Early parts shortlist
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



## Mission States

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



## Final Movement Simulation

The final movement simulation tests how the UAV responds when the landing marker is visible but not yet centered or at the desired apparent size. The simulation uses X and Y position errors to determine how the UAV should move laterally, and it uses marker size to estimate whether the UAV should move closer to or farther from the target. The guidance system prioritizes centering the marker in the camera view before adjusting distance from the marker. Once the marker is centered within the position tolerance, the system uses the marker-size command to adjust the UAV's distance from the target. The simulation stops once the marker is centered and the marker size is within the desired range.

### Simulation Plots
The final movement simulation saves three plots:

* final_movement_error_plot.png shows how the X and Y position errors change over time.
* final_movement_marker_size_plot.png shows how the apparent marker size changes as the UAV adjusts distance from the target.
* final_movement_command_plot.png shows the final X, Y, and Z movement commands produced by the guidance system.
* Together, these plots show that the UAV centers the marker first, adjusts distance second, and stops once the final movement condition is reached.