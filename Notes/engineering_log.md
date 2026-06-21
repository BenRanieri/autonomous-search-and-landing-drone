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