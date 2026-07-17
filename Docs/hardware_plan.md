# Hardware Plan

## Chosen Hardware Path

Primary path: Pixhawk-style flight controller with laptop companion computer.

The Python code will run on the laptop first. The laptop will send high-level movement commands to the flight controller through MAVLink. The flight controller will handle stabilization, sensors, motor control, and safety-critical low-level flight behavior.

The main hardware goal is to build toward a physical autonomous drone capable of running the project’s core mission chain:

TAKEOFF -> SEARCH -> ACQUIRE -> TRACK -> APPROACH -> LAND -> DISARM

LiDAR-based obstacle avoidance is not part of the first hardware order. It may be added later as a future upgrade if the core autonomous flight system is working early enough.

## System Architecture

Laptop / Python autonomy code  
-> Mission and guidance logic  
-> MAVLink command interface  
-> Pixhawk-style flight controller  
-> ESCs and motors  
-> Drone movement

## Build Levels

### Level 1: Bench MAVLink Setup

Goal:  
Test communication between Python code and a real flight controller.

Parts:
- Pixhawk-style flight controller
- USB cable
- Laptop running Python
- MAVLink software/tools

Restrictions:
- No motors
- No propellers
- No battery flight setup

### Level 2: Unpowered Airframe Setup

Goal:  
Mount the flight controller and plan physical layout without spinning motors.

Parts:
- F450-style frame
- Flight controller
- Power module
- GPS/compass if included
- Mounting hardware

Restrictions:
- No propellers installed
- No powered motor tests yet

### Level 3: Full Flight-Capable Build

Goal:  
Build toward a real autonomous quadcopter after bench testing and safety checks.

Parts:
- F450-style frame
- Pixhawk-style flight controller
- Power module
- GPS/compass
- 4 brushless motors
- 4 ESCs or 4-in-1 ESC
- Matched propellers
- LiPo battery
- LiPo charger
- RC transmitter and receiver
- Battery strap / mounting hardware
- Spare props
- Wiring/connectors

## Preliminary Parts List

### Confirmed Direction

The project will use a Pixhawk-style flight-controller architecture with a laptop acting as the first companion computer.

The first hardware goal is not obstacle avoidance. The first hardware goal is autonomous flight-controller communication and a physical drone build that can support the main search-and-landing mission.

### Level 1: Bench MAVLink Setup

| Part | Planned Choice | Status |
|---|---|---|
| Flight controller | Holybro Pixhawk 6C Mini or similar Pixhawk-compatible controller | Likely |
| Power module | PM02-style power module, preferably bundled with flight controller | Likely |
| USB cable | Compatible USB cable for laptop connection | Needed |
| Ground software | Mission Planner / QGroundControl | Needed |
| MAVLink Python library | pymavlink or similar | Needed |

### Level 2: Unpowered Airframe Setup

| Part | Planned Choice | Status |
|---|---|---|
| Frame | F450-style quadcopter frame | Likely |
| Flight-controller mount | Vibration-damping mount or pad | Needed |
| GPS/compass | Compatible GPS/compass module | Likely |
| Battery strap / mounting hardware | Frame-compatible straps and hardware | Needed |

### Level 3: Full Flight-Capable Build

| Part | Planned Choice | Status |
|---|---|---|
| Motors | 4 brushless motors matched to F450 frame, battery, props, and ESCs | TBD |
| ESCs | 4 ESCs or one 4-in-1 ESC matched to motors and battery | TBD |
| Propellers | Props matched to motor KV and frame size | TBD |
| Battery | LiPo battery matched to motor/ESC setup | TBD |
| Charger | LiPo balance charger | TBD |
| RC transmitter | Manual control / safety override transmitter | TBD |
| RC receiver | Receiver compatible with transmitter and flight controller | TBD |
| Spare props | Matched spare propellers | TBD |
| Wiring/connectors | Battery connector, motor/ESC wiring, power wiring | TBD |

## Current Parts Decision

The flight-controller direction is the first major hardware decision.

The Pixhawk 6C Mini is a strong candidate because it is a Pixhawk-style flight controller that supports the type of MAVLink-based autonomy architecture needed for this project.

The exact motor, ESC, propeller, and battery combination is still TBD because those parts must be selected as a matched set.

LiDAR or ToF obstacle sensing will not be included in the first order. It may be added later after the main autonomous flight system is working.

## Current Buying Decision

Do not buy the full motor, ESC, battery, and propeller set until the exact combination is checked.

First priority:
- Flight controller / Pixhawk-style kit
- USB bench-test setup
- F450-style frame or complete compatible frame kit
- Matched motor, ESC, propeller, battery, and charger set after compatibility check
- RC transmitter and receiver for manual override

Reason:  
The flight controller determines how the Python command interface will eventually communicate with real UAV hardware. The motor, ESC, propeller, and battery combination must be selected carefully as a matched set to avoid unsafe or incompatible hardware.

## Budget Planning

Original target budget: about $250.

The chosen Path 2 hardware direction will likely exceed the original budget if a full flight-capable drone is built from new parts. The flight controller alone may take a large part of the budget. For example, the Holybro Pixhawk 6C Mini is listed starting around $130.99, and a Pixhawk 6C Mini with a PM02 V3 power module is listed around $149.98.

### Level 1 Estimated Cost: Bench MAVLink Setup

Goal:  
Test Python-to-flight-controller communication before building the full drone.

Estimated parts:
- Pixhawk-style flight controller: $130-$170
- Power module if not included: $20-$40
- USB cable / small accessories: $0-$15

Estimated total:  
$150-$220

This level is the highest priority because it proves the Python command interface can communicate with real UAV hardware.

### Level 2 Estimated Cost: Unpowered Airframe Setup

Goal:  
Mount the controller and plan the physical layout without spinning motors.

Estimated additional parts:
- F450-style frame: $20-$40
- Mounting hardware / vibration pad / straps: $10-$25

Estimated additional total:  
$30-$65

Estimated running total:  
$180-$285

### Level 3 Estimated Cost: Full Flight-Capable Build

Goal:  
Build toward an actual quadcopter after bench testing and safety checks.

Estimated additional parts:
- 4 brushless motors: $40-$80
- 4 ESCs or 4-in-1 ESC: $30-$70
- Propellers and spare props: $10-$25
- LiPo battery: $25-$50
- LiPo charger: $30-$70
- RC transmitter and receiver: $50-$120
- Miscellaneous wiring, connectors, straps, landing gear: $20-$50

Estimated additional total:  
$205-$465

Estimated full-build total:  
$385-$750

### Budget Conclusion

A complete Pixhawk-style physical drone build will probably exceed the original $250 target if all parts are purchased new.

The practical plan is:
1. Choose the exact flight-controller setup.
2. Choose a compatible frame.
3. Choose the exact motor, ESC, propeller, and battery set as a matched group.
4. Order the hardware early enough to leave time for assembly and debugging.
5. Prove Python-to-MAVLink communication on the bench.
6. Assemble and test the drone in stages.
7. Keep propellers off until all safety checks, manual control, and command behavior are verified.

## Future Add-On: LiDAR Obstacle Avoidance

A forward-facing LiDAR or ToF sensor may be added after the core autonomous flight system is working.

This feature is not required for the first full autonomous flight goal. The first priority is completing the main flight chain:

TAKEOFF -> SEARCH -> ACQUIRE -> TRACK -> APPROACH -> LAND -> DISARM

If time allows after the main flight demo is working, LiDAR obstacle avoidance can be added as a command safety filter.

Possible future behavior:
- Read forward obstacle distance from a dedicated sensor.
- Allow normal mission commands when the path is clear.
- Reduce or stop forward motion when an obstacle is close.
- Override unsafe commands with a stop or sidestep command.

Possible future parts:
- Forward-facing LiDAR or ToF distance sensor
- Sensor mounting hardware
- Wiring/connectors
- Possible USB-to-serial adapter for bench testing

This future add-on should only be attempted after the main autonomous flight hardware and software are already working.

## Safety Notes

- No propellers during bench testing.
- No powered motor tests until the command interface and safety behavior are verified.
- No autonomous flight testing until manual override and emergency stop behavior are planned.
- LiPo batteries require safe charging, storage, and handling.
- Soldering should be practiced on spare wires/connectors before soldering drone power components.
- All motor and ESC tests should begin with propellers removed.
- Manual control and failsafe behavior must be verified before autonomous flight testing.