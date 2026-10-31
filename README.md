# Autonomous Search and Landing UAV

A computer-vision-guided autonomous UAV capable of autonomous takeoff, search, target acquisition, target tracking, and precision landing.

This project combines robotics, aerospace engineering, computer vision, guidance and control, simulation, and hardware integration to develop a complete autonomous aerial mission system.

## Current Flight-Test Status

The project has resumed for its final flight-test window.

Compatible 1045 replacement propellers have been installed and successfully tested in manual flight. The Raspberry Pi vision system, Pixhawk MAVLink connection, safety gate, and ArUco marker detection have also been revalidated after the project pause.

During flight testing, a disconnected Raspberry Pi power solder joint and loose frame/arm hardware were identified as hardware faults. The power connection was repaired and the frame was tightened, significantly improving Stabilize and AltHold flight behavior.

The remaining goal is to complete the read-only sign-mapping flight, validate the real camera-error movement directions, and attempt a safety-gated autonomous run.

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
* Reusable marker detection function
* Marker ID extraction
* Image load error handling
* Marker detection error handling
* Proportional guidance command function
* Controller test script
* Deadband boundary testing
* Command limit boundary testing
* Closed loop controller simulation
* Simulated error correction over time
* Controller response plots
* Marker apparent size calculation
* Desired marker size logic
* Marker size tolerance logic
* Distance-aware guidance logic
* Combined position and size guidance
* Center-first guidance priority logic
* Final movement command loop
* Final movement simulation
* Final movement stress-test evaluation
* Controller parameter tuning comparison
* Conservative default controller baseline
* Physical command interface folder
* Dry-run velocity command function
* Stop command helper
* Command limiting for safe dry-run outputs
* Mission-state update function
* TAKEOFF to SEARCH transition logic
* SEARCH to ACQUIRE transition logic
* ACQUIRE to TRACK transition logic
* TRACK to APPROACH transition logic
* APPROACH to LAND transition logic
* LAND to DISARM transition logic
* Full mission simulation
* MAVLink-ready command-interface structure
* Emergency stop command
* Mission command wrapper
* Hardware plan document
* Preliminary hardware parts list
* Final initial hardware order selected
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
* ArduCopter firmware installation
* Quad X frame configuration
* Accelerometer calibration
* TELEM2 serial setup for ELRS receiver input
* TELEM3 serial setup for Raspberry Pi MAVLink
* Built and mounted major drone hardware components
* Powered RP1 receiver successfully
* Bound receiver to transmitter
* Configured Stabilize, AltHold, and Loiter flight modes
* Configured radio failsafe
* Configured low battery failsafe
* Completed compass calibration
* Successful GPS lock
* Established telemetry radio connection
* Configured motor spin directions
* Installed original propellers with correct motor direction matching
* Manual hover test in Stabilize
* Manual hover test in AltHold
* Manual hover test in Loiter
* Raspberry Pi setup
* Raspberry Pi desktop setup
* Connected camera to Raspberry Pi
* Live ArUco marker detection and error output
* Clean Raspberry Pi ArUco tracker script
* Raspberry Pi camera output converted into detected, marker ID, error X, and error Y values
* Project code organized on Raspberry Pi
* Built Raspberry Pi to Pixhawk TELEM3 UART adapter cable
* Soldered TELEM3 pigtail wires to female jumper ends
* Insulated unused TELEM3 pigtail wires
* Connected Pixhawk TELEM3 ground, transmit, and receive lines to Raspberry Pi GPIO UART
* Connected TELEM3 pigtail red wire to Raspberry Pi physical pin 6 for ground
* Connected TELEM3 pigtail green wire to Raspberry Pi physical pin 8 for TXD / GPIO14
* Connected TELEM3 pigtail blue wire to Raspberry Pi physical pin 10 for RXD / GPIO15
* Verified Raspberry Pi GPIO UART using pin 8 to pin 10 loopback test
* Switched MAVLink connection from `/dev/serial0` to `/dev/ttyAMA0`
* Raspberry Pi vision test scripts added to project repository
* Raspberry Pi GPIO UART setup
* Raspberry Pi UART loopback test
* Raspberry Pi to Pixhawk TELEM3 MAVLink connection
* MAVLink heartbeat test between Raspberry Pi and Pixhawk
* Pixhawk telemetry stream request from Raspberry Pi
* Raspberry Pi Pixhawk read-only status test
* Combined Raspberry Pi camera and Pixhawk read-only integration test
* Dry-run vision and guidance integration test
* ArUco marker error conversion into proportional dry-run tracking commands
* MAVLink commands kept disabled during dry-run testing
* Mission-state dry-run logger
* SEARCH to ACQUIRE dry-run transition using live ArUco detection
* ACQUIRE to TRACK dry-run transition using marker centering stability
* TRACK to APPROACH dry-run transition using marker tracking stability
* Marker size estimation for approach logic
* APPROACH to LAND dry-run transition using marker centering and marker size
* LAND to DISARM dry-run transition using fake software altitude
* Full dry-run mission sequence from SEARCH to DISARM
* Command safety gate dry-run test
* Reusable command safety gate module
* Safety-gated MAVLink command wrapper
* Basic bounded search pattern
* Command-wrapper search dry-run test
* Combined search, mission, and command-wrapper dry-run test
* SEARCH pattern stopping on ArUco marker detection
* Full safety-gated dry-run mission sequence from SEARCH to DISARM
* Raspberry Pi temporary onboard mounting
* Front-mounted camera setup for precision landing tests
* Raspberry Pi flight-power wiring through LiPo splitter and 5V buck converter
* Raspberry Pi boot and Pixhawk communication from flight-power wiring
* Safety-wrapper search dry-run test while Raspberry Pi was powered from flight wiring
* Front-mounted camera offset calibration
* Mounted camera guidance module using calibrated drone-center target offset
* Mounted offset mission dry-run from SEARCH to DISARM
* Onboard read-only flight logger for marker, telemetry, and suggested guidance logging
* Flight safety gate wording updated for future real-flight testing
* Sign-mapping read-only logger for manual flight testing
* Next-session read-only flight checklist
* Sign-mapping log analyzer
* GitHub update with latest safety, logging, checklist, and analysis code
* Amazon 1045R and 1045L replacement propeller inspection
* Propeller nut fit check on threaded motor shafts
* CW and CCW propeller placement mapping for known motor spin directions
* Front left and back right motors matched to 1045R propellers
* Front right and back left motors matched to 1045L propellers
* Generic 1045 propeller mounting compatibility check
* Determined that generic through-hole 1045 propellers cannot safely clamp onto the current short threaded motor shafts
* Rejected unsafe propeller mounting methods such as placing nuts under the propellers or forcing nuts into the propeller hubs
* Identified threaded-hub or self-locking 1045 propellers as the required replacement style
* Defined current project state as a bench-validated autonomous search-and-landing UAV prototype
* Established flight testing pause point pending exact compatible propeller replacement
* Received and installed compatible 1045 replacement propellers
* Verified new propeller fit, direction, and secure mounting
* Successful manual flight test using the replacement propellers
* Regained Raspberry Pi access and restored field-development workflow
* Configured Raspberry Pi Wi-Fi hotspot for direct laptop-to-Pi SSH access during field testing
* Re-ran command safety gate test and confirmed all unsafe command cases remain blocked
* Re-ran Raspberry Pi live ArUco test and confirmed marker ID 0 detection and position-error output
* Re-ran Raspberry Pi and Pixhawk read-only integration test
* Confirmed Pixhawk heartbeat and live ArUco detection through the onboard Raspberry Pi
* Diagnosed Raspberry Pi power failure as a disconnected solder joint after a crash
* Repaired Raspberry Pi power connection
* Diagnosed poor Stabilize and AltHold behavior as loose frame and arm hardware
* Tightened frame and motor-arm hardware
* Re-tested manual flight after frame repair and confirmed substantially improved stabilization
* Completed the first outdoor full-mission flight test with live GUIDED commands
* Verified the autonomous SEARCH behavior can consistently locate and reacquire the ArUco landing target
* Verified successful transition from SEARCH to CENTER during real flight
* Replaced the NoIR camera with an IR-cut Raspberry Pi camera for improved daytime vision
* Increased the ArUco landing marker to approximately 8 in by 8 in and mounted it on matte poster board
* Increased the CENTER marker-loss grace period from 1 second to 2 seconds
* Recalibrated the mounted camera after the camera replacement
* Achieved 100% ArUco detection in a 191-frame stationary reliability test

### In Progress

* Diagnosing unreliable ArUco detection during live flight despite stable stationary detection
* Verifying the physical X and Y command-direction mapping used by the CENTER guidance
* Inspecting and repairing the drone after a failed live centering test

### Planned

* Replace all four damaged propellers and inspect the airframe and electronics for crash damage
* Reconfirm normal manual and Loiter flight before additional autonomous testing
* Validate CENTER command directions with props removed
* Resolve the live marker-detection and guidance-direction issues before another autonomous centering test


## System Architecture

Raspberry Pi 5 / Python Autonomy Code

↓

Computer Vision

↓

ArUco Target Detection

↓

Marker Position and Size Estimation

↓

Mission and Guidance Logic

↓

Safety-Gated MAVLink Command Interface

↓

Pixhawk 6C Flight Controller

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

The project uses a Pixhawk-style flight-controller architecture with a Raspberry Pi 5 acting as the onboard companion computer.

The Raspberry Pi runs Python autonomy, camera, logging, and MAVLink communication code. The Pixhawk handles stabilization, low-level flight control, motor outputs, and safety-critical flight behavior.

The current onboard autonomy stack supports the main mission chain:

SEARCH → ACQUIRE → TRACK → APPROACH → LAND → DISARM

Autonomous takeoff, LiDAR-based obstacle avoidance, and fully unattended flight are future work. The current pause point focuses on bench-validated perception, mission logic, safety-gated command generation, and flight-test preparation.



## Final Movement Simulation

The final movement simulation tests how the UAV responds when the landing marker is visible but not yet centered or at the desired apparent size. The simulation uses X and Y position errors to determine how the UAV should move laterally, and it uses marker size to estimate whether the UAV should move closer to or farther from the target. The guidance system prioritizes centering the marker in the camera view before adjusting distance from the marker. Once the marker is centered within the position tolerance, the system uses the marker-size command to adjust the UAV's distance from the target. The simulation stops once the marker is centered and the marker size is within the desired range.

### Simulation Plots
The final movement simulation saves three plots:

* final_movement_error_plot.png shows how the X and Y position errors change over time.
* final_movement_marker_size_plot.png shows how the apparent marker size changes as the UAV adjusts distance from the target.
* final_movement_command_plot.png shows the final X, Y, and Z movement commands produced by the guidance system.
* Together, these plots show that the UAV centers the marker first, adjusts distance second, and stops once the final movement condition is reached.