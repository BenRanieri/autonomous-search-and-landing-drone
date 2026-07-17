# Autonomous Search and Landing UAV

## Project Objective

Develop an autonomous unmanned aerial vehicle capable of performing a complete search-and-landing mission with minimal human intervention.

The UAV will autonomously:

1. Take off from the ground.
2. Climb to a predefined altitude.
3. Search a designated area for a visual target.
4. Detect and identify an ArUco landing marker.
5. Track and approach the target.
6. Perform a controlled descent toward the target.
7. Land on or near the target.
8. Disarm or stop safely after landing.

The first priority is completing the core autonomous flight chain:

TAKEOFF -> SEARCH -> ACQUIRE -> TRACK -> APPROACH -> LAND -> DISARM

## Minimum Success Criteria

The project will be considered minimally successful if it can:

* Detect ArUco markers using OpenCV.
* Determine target position within the camera image.
* Estimate target alignment using marker center error and marker size.
* Generate guidance commands from target position and size.
* Simulate autonomous target approach.
* Simulate the full mission sequence from takeoff through landing.
* Demonstrate a safe command interface that can send dry-run movement commands.

## Target Success Criteria

The target goal is to demonstrate the full autonomy pipeline on hardware.

The UAV should support:

* Autonomous takeoff logic.
* Autonomous hover or hold behavior.
* Autonomous search behavior.
* Autonomous target acquisition.
* Autonomous target tracking.
* Autonomous approach behavior.
* Controlled descent toward the landing marker.
* Autonomous landing or near-target landing.
* Safe stop or disarm behavior after landing.
* MAVLink-based communication with a Pixhawk-style flight controller.
* Operation on a physical drone if hardware testing is safe and successful.

## Hardware Success Criteria

The hardware system should demonstrate:

* Pixhawk-style flight controller setup.
* Laptop companion-computer architecture.
* Python-to-flight-controller communication through MAVLink.
* Bench testing with no propellers installed.
* Props-off command testing before any powered flight.
* Manual override or safety control method before autonomous flight.
* Physical drone assembly sufficient for controlled testing.
* Limited autonomous physical flight if safety checks are passed.

## Safety Requirements

The project must follow these safety requirements:

* Propellers must stay removed during bench testing and command-interface testing.
* Motor tests must begin with propellers removed.
* LiPo batteries must be handled, charged, and stored safely.
* Manual override or emergency stop behavior must be planned before autonomous flight.
* Autonomous flight testing must only occur after hardware, software, and failsafe checks.
* Full autonomous testing should be attempted only in a safe, open, controlled environment.

## Future Work

These features may be added after the core autonomous flight system is working:

* LiDAR-based obstacle avoidance.
* Kalman-filter-based target tracking.
* Wind disturbance rejection.
* Dynamic target tracking.
* Multiple marker support.
* Custom UAV frame design.
* More advanced search patterns.
* Improved landing precision.

### LiDAR-Based Obstacle Avoidance

A forward-facing LiDAR or ToF sensor may be added after the core autonomous flight system is working.

This feature is not required for the first full autonomous flight goal. The first priority is completing the main autonomous flight chain:

TAKEOFF -> SEARCH -> ACQUIRE -> TRACK -> APPROACH -> LAND -> DISARM

If time allows after the main flight demo is working, LiDAR obstacle avoidance can be added as a command safety filter.

## Engineering Disciplines Demonstrated

* Robotics
* Computer Vision
* Guidance, Navigation, and Control (GNC)
* Aerospace Systems Engineering
* Autonomous Systems
* Flight Control
* Embedded Systems
* Simulation and Testing
* Hardware Integration
* Safety-Critical System Design