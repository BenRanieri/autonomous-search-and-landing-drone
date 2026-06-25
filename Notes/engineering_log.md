# Engineering Log

## Session 1 - June 9, 2026
### Accomplished
- Created GitHub repository
- Installed Python
- Created virtual environment
- Installed OpenCV, NumPy, and Matplotlib
- Created first image loading program

### Problems
- VS Code wasn't using the virtual environment
- OpenCV couldn't find the image because of the file path
- Webcam not accessible through WSL

### Solutions
- Selected correct Python interpreter
- Fixed image path
- Decided to postpone webcam setup

### Next Session
- How does an ArUco marker work?
- How can an ArUco marker be read?





## Session 2 - June 11, 2026
### Accomplished
- Learned how ArUco detection works
- Generated a marker with ID 0
- Successfully detected marker ID 0
- Retrieved marker corner coordinates

### Problems:
- Marker without border could not be detected

### Debugging:
- Verified image loaded correctly.
- Verified detector object creation.
- Printed rejected candidate count.
- Determined marker required surrounding white border.

### Solution:
- Added white border around marker image

### Next Session
- How do i use the marker corner coordinates to find position errors for the drone?




## Session 3 - June 12, 2026
### Accomplished
- Extracted individual marker corner coordinates
- Calculated marker center coordinates from corner coordinates
- Calculated image center coordinats
- Learned how OpenCV stores marker data
- Visualized detected marker outline
- Visualized marker center point

### Problems
- Confusion with understanding nested corner array structure
- OpenCV drawing functions not accepting floating-point values
- Marker visualizations difficult to see with default values

### Debugging
- Printed corner array type and dimensions
- Examiend individual corner coordinates
- Investigated OpenCV drawing function documentation
- Tested different circle/outline sizes and colors

## Solution
- Extracted coordinates from corner array piecewise
- Converted center coordinates to integer values using rounding
- Added visual overlays to verify calculations
- Increased circle size and color for visibility

## Next Session
- How can position errors generate guidance commands?
- How should the UAV respond when a target is offset from the center?





## Session 4 - June 13, 2026
### Accomplished
- Designed guidance logic using errorX and errorY
- Added movement commands for left, right, forward, backward, and maintain
- Added a tolerance to ignore small errors
- Converted guidance logic into a usable function with parameters
- Created test cases for guidance function
- Incorporated guidance function to detect_marker.py
- Replaced image display with saved image output

### Problems
- Buildup of different types of code in one folder
- Unsure of use cases for printing values and returning values
- OpenCV imshow() command produced font warning in terminal
- Needed to access a function from Guidance folder in the Vision folder

### Debugging
- Tested positive and negative errorX values
- Tested positive and negative errorY values
- Tested small errors inside and outside of tolerance
- Tested the various test cases on function
- Confirmed final marker visualization can be saved as an image

### Solution
- Put decision making code in Guidance folder
- Used a tolerance of 10 pixels
- Returned commandX and commandY from guidance function
- Printed returned commandX and commandY in detect_marker.py
- Replaced cv2.imshow() with cv2.imwrite()

### Next Session
- Can my other code be packaged into functions?
- How can the vision to guidance pipeline be improved?
- How does this relate to a proportional controller?





## Session 5 - June 15, 2026
### Accomplished
- Refactored marker detection code into configurable function
- Added separate function path for saving marker visualization
- Added markerID as a return
- Added error handling for image loading errors
- Added error handling for no marker detection errors
- Added conditional test cases to separate test cases from function
- Added NumPy style array indexing for marker center calculation
- Confirmed function handles all intended cases correctly

### Problems
- Original marker detection became too long of a script
- Variables needed for visualization unusable outside of function
- Code would crash if image path or marker detection errors
- Marker center calculation manually extracted every corner coordinate
- Visualization code was disruptive if not optional

### Debugging
- Tested function with ArUco marker image
- Tested function with fake image path
- Tested no marker case
- Confirmed None values prevented guidance function from running
- Compared rewritten marker center calculations to old calculations
- Tested enabling and disabling optional marker visualization

### Solution
- Wrapped marker detection and error calculation into detect_marker_position()
- Returned None variables when image path or marker detection error
- Used .mean() and array indexing to calculate marker center
- Added saveVisualization as boolean input to decide if image should be visualized

### Next Session
- How can guidance commands become stronger or weaker based on error values?
- How can errorX and errorY be converetd into movement strength?





## Session 6 - June 16, 2026
### Accomplished
- Created a new proportional command function for guidance
- Added a kp input to proportional command function
- Added a max command input to limit command strength
- Created test cases to ensure proportional command worked with marker errors
- Created test cases to ensure proportional command worked with simulated errors
- Connected the proportional command function to the marker detection pipeline

### Problems
- Original guidance function outputted only string instructions
- Error values needed to still respect the set tolerance
- Proportional command function were unrestricted originally
- Updating function signature caused old function calls to become invalid
- Limiting command size needed to preserve original command sign

### Debugging
- Tested function with original ArUco marker image
- Tested function with simulated offset errors
- Tested function with small errors within tolerance
- Tested functions with errors greater than maxiumum command value
- Tested function calls before changing to new function signature

### Solution
- Created a new function with numeric command outputs
- Added tolerance logic to set small error commands to zero
- Added proportional gain using kp
- Added maxCommand logic to cap command size
- Updated old function calls to match new function signature
- Preserved sign of command values after limiting their magnitude

### Next Session
- How can proportional command outputs be tested with multiple marker positions?
- How can simulated marker errors be used to evaluate controller behavior?
- How can controller output be logged for debugging?





## Session 7 - June 17, 2026
### Accomplished
- Created test_controller.py in guidance folder
- Imported get_guidance_command and get_proportional_controller
- Created test cases for different errorX and errorY values
- Tested deadband and maximum command cases
- Added controller region labels for deadband, proportional, and capped behavior
- Confirmed string commands and numeric commands match expected behavior

### Problems
- Initial test case list was missing commas between tuples
- Proportional controller and string controller did not agree on tolerance boundary behavior
- Proportional controller used < tolerance while string controller used <= tolerance
- Difficulty telling if test cases were in the deadband, proportional, or capped region

### Debugging
- Ran test cases with zero and small errors
- Ran test cases with positive and negative errorX and errorY values
- Tested values exactly at the tolerance boundary
- Tested values bordering the tolerance boundary
- Tested values at the command limit
- Tested values bordering the command limit
- Compared string outputs to numeric outputs
- Added printed controller region labels to make test output easier to read

### Solution
- Fixed test case list formatting
- Changed proportional deadband logic to match <= tolerance
- Confirmed deadband error logic in strings and numbers matched
- Confirmed errors outside tolerance range produced proportional commands
- Added a helper function to classify controller behavior as deadband, proportional, or capped

### Next Session
- How can controller behavior be tested with simulated marker movement over time?
- How can marker error change as the drone corrects its position?
- How can the controller output be used to update a simple simulated drone position





## Session 8 - June 18, 2026
### Accomplished
- Created simulate_controller.py in Guidance folder
- Imported get_proportional_controller from guidance_logic.py
- Built a simple closed loop controller simulation
- Started simulation with fake marker error values
- Ran proportional controller over multiple time steps
- Updated errorX and errorY values based on controller output
- Added stop condition for when target enters tolerance zone
- Added targetCentered flag to track if simulation was success
- Added multiple test cases
- Refactored simulation into run_simulation() function
- Added printSteps boolean input for detailed output

### Problems
- The first simulation loop repeated the same error value since no updating
- One test case did not center within original number of steps
- Running multiple test cases required changing starting error values manually
- Printing every step for every test case made output hard to read

### Debugging
- Ran the controller once to confirm proportional commands correct
- Ran the controller inside a loop to test repeated command generation
- Added simulated error updates using correctionScale
- Tested whether simulated marker error decreased over time or not
- Added a tolerance based stop condition once centered
- Increased numSteps so larger errors had time to converge
- Tested several starting error cases with positive, negative, large, and centered errors
- Verified all test cases ended inside tolerance range

### Solution
- Added simulated correction updates based on controller output
- Added a success condition using abs(errorX/Y) <= tolerance
- Added a targetCentered flag to distinguish success and running out of steps
- Added printSteps to separate detailed output for summary testing
- Confirmed proportional controller consistently drives marker error into tolerance

### Next Session
- How can the simulated controller response be visualized?
- How can error values be stored during simulation?
- How can controller behavior be evaluated using visualizations?





## Session 9 - June 20, 2026
### Accomplished
- Added history tracking to the controller simulation
- Created stepHistory, errorXHistory, errorYHistory, xCommandHistory, and yCommandHistory
- Stored simulated error values at each controller step
- Stored proportional command outputs at each controller step
- Updated run_simulation() to return simulation history values
- Created an error response plot for errorX and errorY
- Added positive and negative tolerance lines to the error plot
- Created a command response plot for xCommand and yCommand
- Saved the error plot as controller_error_plot.png
- Saved the command plot as controller_command_plot.png
- Closed each plot after saving it

### Problems
- The simulation only returned final result, therefore no way to visualize over time behavior
- The plotting code required the simulation to return history lists instead of final values
- Confusion on where the plotting code belonged within the script
- Multiple plots needed to be saved without interferance

### Debugging
- Added history lists without changing other simulation behavior
- Confirmed simulation had same results after changes
- Returned history lists from run_simulation()
- Created error plots to verify error lines entered tolerance band
- Created the command plot to check for decreasing command values over time
- Added plt.close() to separate the figures

### Solution
- Stored error and command values during each simulation step
- Used Matplotlib to plot error over time
- Used dashed horizontal lines to show tolerance boundaries
- Saved both plots to Guidance folder
- Confirmed controller drives simulated marker error into tolerance
- Confirmed the controller commands decreased as error became smaller

### Next Session
- How can the marker apparent size estimate distance from target?
- How can distance aware behavior be added to the controller
- How can the UAV decide when to approach, descend, or hold position?





## Session 10 - June 21, 2026
### Accomplished
- Added marker apparent size calulcation to detect_marker.py
- Extracted four detected marker corners
- Calculated the top, bottom, left, and right marker side lengths
- Computed markerSize as average of the side lengths
- Updated detect_marker_position to return markerSize
- Updated error detection returns to include four None variables
- Printed detected marker size in test case
- Added get_size_command() to guidance_logic.py
- Added desiredSize and sizeTolerance variables
- Connected marker size command to detect_marker

### Problems
- Marker size value was calculated but not printed
- get_size_command() used two if statements instead of if and elif
- Old test case comments had outdated command names and calls
- Maintain case overwrote the closer case when marker was small

### Debugging
- Printed markerSize from detect_marker.py
- Confirmed detected marker size was 399 pixels
- compared detected marker size to known corner positions
- Tested fake marker size below, inside, and above desired size
- Found 250 returned maintain instead of closer
- Identified second if statement caused else statement to ignore first if
- Replaced second if with elif
- Re-ran fake marker size tests to confirm correct outputs

### Solution
- Calculated marker apparent size by averaging detected size lengths
- Returned markerSize from marker detection function
- Used desiredSize and sizeTolerance to define acceptable size range
- Used if/elif/else so only one conditional branch runs
- Confirmed marker image gave a size of 399 pixels and returns maintain

### Next Session
- How can marker size commands be turned into numeric appraoch and descent commands?
- How can position control and size control be combined into one guidance output?
- How can the UAV decide whether to center or approach first?





## Session 11 - June 22, 2026
### Accomplished
- Added a combined guidance function to guidance_logic.py
- Created get_combined_guidance() using commandX, commandY, and sizeCommand
- Set the combined guidance priority to center the marker before adjusting distance
- Added logic for centered, closer, further, and maintain cases
- Tested combined guidance with fake command values
- Imported get_combined_guidance() into detect_marker.py
- Printed the combined command in the marker detection output
- Confirmed the combined command responds correctly to maintain, closer, and further cases

### Problem
- Combined guidance needed priority order
- Temporary test print statements would have made guidance_logic.py run tests every time it was imported
- Fake size settings were needed to test closer and further behavior

### Debugging
- Tested combined guidance with fake command inputs
- Confirmed that non-maintain X or Y commands produce a center command
- Confirmed that centered position with a small marker-size condition produces a closer command
- Confirmed that centered position with a large marker-size condition produces a further command
- Confirmed that centered position with acceptable marker size produces maintain
- Ran detect_marker.py with the real marker image

### Solution
- Added get_combined_guidance() to combine position and size guidance
- Used position guidance as the first priority
- Used size guidance only after X and Y position commands were both maintain
- Returned one high-level combined command from the separate guidance outputs
- Connected the combined command to the real marker detection pipeline

### Next Session
- How can combined guidance commands become numeric movement commands?
- How can closer and further become approach/descent behavior?
- How can combined guidance be a foundation for mission state logic?





## Session 12 - June 23, 2026
### Accomplished
- Designed the final numeric movement command structure
- Added get_elevation_command() to convert size commands into numeric Z commands
- Used approachCommand as a fixed numeric strength for closer and further movement
- Tested closer, further, and maintain elevation outputs
- Added get_final_movement() to combine high-level guidance with numeric movement commands
- Tested final movement outputs for center, closer, further, and maintain cases
- Connected the final movement command chain into detect_marker.py
- Tested forced closer and further cases using temporary desired-size changes

### Problems
- The Z command needed its own numeric conversion before being used in the final movement function
- approachCommand needed to be defined as a fixed tuning value rather than an image-derived value
- A conditional statement using or "further" would have always evaluated as true
- Temporary test print statements appeared in the output before the real marker detection output

### Debugging
- Separated size-command interpretation from final movement generation
- Tested get_elevation_command() with closer, further, and maintain inputs
- Fixed the final movement conditional by checking whether combinedCommand was closer or further correctly
- Tested final movement outputs for center, closer, further, and maintain cases
- Removed temporary test print statements after confirming expected outputs
- Ran detect_marker.py with the real marker image
- Temporarily changed desiredSize to force closer and further cases
- Restored the desired marker size after testing

### Solution
- Added a numeric elevation command function for distance adjustment
- Used negative Z for closer or descent behavior
- Used positive Z for further or increase-distance behavior
- Added a final movement command function to output numeric X, Y, and Z commands
- Used proportional X and Y commands only when the combined command is center
- Used Z movement only when the combined command is closer or further
- Used zero movement for maintain
- Confirmed that forced closer and further cases produce the correct final Z commands

### Next Session
- How can final movement commands be tested in simulation over time?
- How can X, Y, and Z command histories be stored and plotted
- How can final movement outputs become the foundation for mission state logic





## Session 13 - June 24, 2026
### Accomplished
- Created simulate_final_movement.py in Guidance
- Imported full guidance function chain
- Added controller tuning for tolerance, gain, max commands, desired size, tolerance, and approach
- One step final movement command calculation
- Built a loop to simulate X, Y, and Z over time
- updated simulated errorX, errorY, and markerSize in loop
- Added stopping conditions
- Confirmed simulation centers, then adjusts distance through test cases

### Problems
- First one step output had string commands and numeric outputs assigned to wrong variables
- First loop version had no clear stopping condition
- Simulation had no way to prevent movement after target was centered and sized

### Debugging
- Printed all intermediate guidance outputs to see command chain
- Compared get_guidance_command() outputs to get_proportional_command() outputs
- Fixed variable assignment order
- Verified off center targets produced correct output
- Verified Z movement stayed zero while off centered
- Added simulated updates for X, Y, and marker size
- Added loop condition with maxSteps
- Added a success check when X, Y, and Z reached 0
- Tested cases with marker being too large and marker being too small

### Solution
- Created a full simulation of final movement command pipeline
- Used final X and Y to reduce position error
- Used final Z to change marker size
- Demonsrated the full behavior sequence: center then adjust distance then maintain
- Confirmed simulation stops with both end conditioms

### Next Session
- How can movement simulation be refactored into a reusable function?
- How can multiple starting cases be tested automatically?
- How can final X, Y, Z, error, and size histories be stored and plotted?





## Session 14 - June 25, 2026
### Accomplished
- Refactored simulate_final_movement.py into a reusable simulation function
- Created run_movement_simulation()
- Moved the final movement simulation loop inside the function
- Initialized errorX, errorY, markerSize, and step inside the function
- Returned final errorX, errorY, markerSize, xFinal, yFinal, and zFinal
- Added an import-friendly if __name__ == "__main__": test section
- Added multiple starting test cases
- Added short final summary output for each test case
- Confirmed that all test cases ended centered and at the correct simulated distance

### Problems
- The first refactor was missing markerSize = startingMarkerSize inside the function
- desiredSize was initially misspelled in the function input list
- The simulation needed useful return values so final results could be summarized outside the function
- The test code needed to be placed under if __name__ == "__main__": so importing the function would not automatically run test cases
- One summary print line accidentally printed startingMarkerSize as the starting X error
- A leftover step = 0 outside the function was no longer needed

### Debugging
- Compared the refactored function output against the original script output
- Added final return values from the simulation function
- Ran the simulation with detailed step printing to confirm behavior still matched Session 13
- Switched to printSteps = False for shorter multi-case testing
- Added several starting cases to test different behavior paths
- Checked that final X, Y, and Z movement commands ended at zero
- Checked that final position errors ended inside the tolerance band
- Checked that final marker sizes ended inside the desired size range
- Fixed the incorrect starting error print statement

### Solution
- Converted the final movement simulation into a reusable function
- Kept the simulation file import-friendly
- Added automatic testing over multiple starting conditions
- Returned final simulation values for clean summary output
- Confirmed that all tested cases end with final movement 0, 0, 0
- Confirmed that the simulation remains ready for future history tracking and plotting

### Next Session
- How can final movement histories be stored during simulation?
- How can X, Y, Z, error, and markerSize values be plotted over time?
- How can simulation plots evaluate guidance behavior?