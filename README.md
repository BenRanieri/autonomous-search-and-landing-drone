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
* Controller parameter tuning comparison
* Multiple final movement parameter sets
* Tuning step-count comparison
* Conservative default controller baseline
* Physical command interface folder
* Dry-run velocity command function
* Stop command helper
* Command limiting for safe dry-run outputs
* Connection from final movement simulation to command interface
* Mission-state update function
* TAKEOFF to SEARCH transition logic
* State-based command generation
* Mission command connection to dry-run command interface
* Simulated altitude update logic
* Autonomous takeoff simulation loop
* TAKEOFF to SEARCH simulated transition
* maxSteps takeoff safety limit
* Safe stop behavior for failed takeoff
* Basic full mission simulation
* TAKEOFF to SEARCH to ACQUIRE mission sequence
* Marker-detection-aware mission-state logic
* SEARCH to ACQUIRE transition
* Mission-guidance integration for ACQUIRE
* get_acquire_command() guidance bridge
* ACQUIRE command tests with simulated marker errors
* Dry-run ACQUIRE movement commands through command interface
* Early hardware path comparison
* Hardware plan document
* Preliminary hardware parts list
* Final initial hardware order selected
* ACQUIRE completion check
* Marker acquisition stability counter
* ACQUIRE to TRACK transition logic
* TRACK command function
* TRACK position correction behavior
* TRACK lost-marker counter
* TRACK marker-loss detection logic
* TRACK to SEARCH lost-marker transition
* Temporary marker-loss recovery behavior
* TRACK ready for approach check
* TRACK stability counter
* TRACK to APPROACH transition logic
* readyToApproach mission-state input
* APPROACH command function
* APPROACH position correction behavior
* APPROACH marker-size distance behavior
* approachComplete output
* Hardware inventory
* S500 frame and mechanical parts confirmed
* ESCs, motors, Pixhawk, GPS, power module, and telemetry radios confirmed
* Amazon support parts confirmed
* Preliminary hardware wiring map
* LiPo battery voltage checking
* LiPo voltage checker use
* Battery safety workflow
* Drone hardware assembly
* Power module placement and connection planning
* Main Pixhawk wiring progress
* APPROACH to LAND transition
* LAND command behavior
* LAND to DISARM transition
* DISARM state behavior
* Full mission simulation
* MAVLink-ready command-interface structure
* Emergency stop command
* Mission command wrapper
* Mission code command-interface integration
* ArduCopter firmware installation
* Quad X frame configuration
* Accelerometer calibration
* TELEM2 serial setup for ELRS receiver input
* TELEM3 serial setup for Raspberry Pi MAVLink
- Built and mounted major drone hardware components
- Flashed Pixhawk 6C from PX4 firmware to ArduCopter
- Configured frame as Quad X
- Completed accelerometer calibration
- Configured TELEM1 for telemetry radio
- Configured TELEM2 for ELRS receiver input
- Configured TELEM3 for future Raspberry Pi MAVLink connection
- Wired RP1 receiver to Pixhawk TELEM2
- Corrected RP1 receiver wiring after identifying the correct TELEM2 pin order
- Powered RP1 receiver successfully
- Bound RadioMaster Pocket ELRS transmitter to RP1 receiver using ExpressLRS Wi-Fi binding phrase
- Confirmed ExpressLRS connection with solid green RP1 LED and C indicator on transmitter
- Confirmed Mission Planner receives radio input from transmitter sticks
- Completed radio calibration in Mission Planner

### In Progress

- Pixhawk flight controller setup and safety configuration
- RC transmitter switch setup
- Flight mode configuration
- Failsafe configuration
- Compass calibration

### Planned

- Finish compass calibration with longer USB cable or telemetry link
- Configure flight modes
- Configure RC and battery failsafes
- Verify motor order and motor direction with props removed
- Complete Raspberry Pi and camera setup for autonomous landing
- Connect companion computer to Pixhawk through MAVLink
- Perform controlled ground tests before any flight testing



## System Architecture

Laptop / Python Autonomy Code  
↓  
Computer Vision  
↓  
Target Detection  
↓  
Position Estimation  
↓  
Mission and Guidance Logic  
↓  
MAVLink Command Interface  
↓  
Pixhawk-Style Flight Controller  
↓  
ESCs and Motors  
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



## Hardware Direction

The project will use a Pixhawk-style flight-controller architecture with the laptop acting as the first companion computer.

The Python autonomy code will run on the laptop and send high-level movement commands through a MAVLink command interface. The flight controller will handle stabilization, low-level flight control, motor outputs, and safety-critical flight behavior.

The first hardware goal is to support the main autonomous mission chain:

TAKEOFF → SEARCH → ACQUIRE → TRACK → APPROACH → LAND → DISARM

LiDAR-based obstacle avoidance has been moved to future work. It may be added after the core autonomous flight system is working.



## Final Movement Simulation

The final movement simulation tests how the UAV responds when the landing marker is visible but not yet centered or at the desired apparent size. The simulation uses X and Y position errors to determine how the UAV should move laterally, and it uses marker size to estimate whether the UAV should move closer to or farther from the target. The guidance system prioritizes centering the marker in the camera view before adjusting distance from the marker. Once the marker is centered within the position tolerance, the system uses the marker-size command to adjust the UAV's distance from the target. The simulation stops once the marker is centered and the marker size is within the desired range.

### Simulation Plots
The final movement simulation saves three plots:

* final_movement_error_plot.png shows how the X and Y position errors change over time.
* final_movement_marker_size_plot.png shows how the apparent marker size changes as the UAV adjusts distance from the target.
* final_movement_command_plot.png shows the final X, Y, and Z movement commands produced by the guidance system.
* Together, these plots show that the UAV centers the marker first, adjusts distance second, and stops once the final movement condition is reached.