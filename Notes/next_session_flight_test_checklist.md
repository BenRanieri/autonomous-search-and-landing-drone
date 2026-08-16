# Next Session Flight Test Checklist

## Purpose

Prepare for the first real read-only flight with the Raspberry Pi mounted and flight-powered

No autonomous movement commands will be sent during this test

## Required Before Flight

* Correct compatible propellers or propeller nuts must be installed
* Propellers must be physically secure
* Propeller direction must match motor spin direction
* Raspberry Pi must boot from flight-power wiring
* Pixhawk must connect to Raspberry Pi over MAVLink
* Camera must be mounted and aimed downward
* Camera ribbon and power cables must be clear of all propellers
* Battery must be charged enough for a short test flight
* Transmitter must be on before connecting the LiPo
* Flight area must be open and clear
* Manual override must be available at all times

## Known Motor Directions

* Front right motor: CCW
* Back right motor: CW
* Back left motor: CCW
* Front left motor: CW

## Propeller Installation Checks

* Install props only with the LiPo disconnected
* Do not use improvised propeller hardware
* Do not use props that wobble on the shaft
* Do not use nuts that cross-thread or only grab a few threads
* Confirm each prop sits flat on the motor
* Confirm each prop is tightened securely
* Confirm CW and CCW props are installed on the matching motors

## Logger Command For Read-Only Flight

Run the sign-mapping read-only logger before takeoff

The logger should run for 110 seconds and write console output to logs/latest_sign_mapping_console.txt

## Manual Flight Plan

* Take off manually
* Hover near the marker in Loiter or AltHold
* Keep the first flight short
* Do not use GUIDED
* Do not run real command scripts
* Keep the drone close and low
* Land manually if anything feels wrong

## Sign-Mapping Flight Sequence

The logger labels these phases automatically:

* GROUND_CHECK
* CENTER_HOVER
* MOVE_FORWARD
* CENTER_HOVER
* MOVE_BACKWARD
* CENTER_HOVER
* MOVE_RIGHT
* CENTER_HOVER
* MOVE_LEFT
* MANUAL_LAND

During the movement phases, move only slightly and slowly

## After Landing

* Disarm manually
* Check logger output
* Confirm the CSV file saved
* Shut down the Raspberry Pi safely before unplugging the LiPo
* Wait 20 to 30 seconds before unplugging the LiPo

## Data Needed From Flight

* Whether marker is detected in real flight
* Marker size at hover height
* How error_x changes when moving left and right
* How error_y changes when moving forward and backward
* Whether mounted camera offset still works in flight
* Whether command signs need to be flipped before real autonomous centering
