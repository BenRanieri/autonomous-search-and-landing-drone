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

### Debugging
- Checked which Python interpreter VS Code was using
- Tested the image file path
- Confirmed the webcam was not accessible through WSL

### Solution
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

### Problems
- Marker without border could not be detected

### Debugging
- Verified image loaded correctly
- Verified detector object creation
- Printed rejected candidate count
- Determined marker required surrounding white border

### Solution
- Added white border around marker image

### Next Session
- How do I use the marker corner coordinates to find position errors for the drone?





## Session 3 - June 12, 2026

### Accomplished
- Extracted individual marker corner coordinates
- Calculated marker center coordinates from corner coordinates
- Calculated image center coordinates
- Learned how OpenCV stores marker data
- Visualized detected marker outline
- Visualized marker center point

### Problems
- Confusion with understanding nested corner array structure
- OpenCV drawing functions not accepting floating-point values
- Marker visualizations difficult to see with default values

### Debugging
- Printed corner array type and dimensions
- Examined individual corner coordinates
- Investigated OpenCV drawing function documentation
- Tested different circle/outline sizes and colors

### Solution
- Extracted coordinates from corner array piecewise
- Converted center coordinates to integer values using rounding
- Added visual overlays to verify calculations
- Increased circle size and color for visibility

### Next Session
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
- How can errorX and errorY be converted into movement strength?





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
- Proportional command functions were unrestricted originally
- Updating function signature caused old function calls to become invalid
- Limiting command size needed to preserve original command sign

### Debugging
- Tested function with original ArUco marker image
- Tested function with simulated offset errors
- Tested function with small errors within tolerance
- Tested functions with errors greater than maximum command value
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
- Imported get_guidance_command and get_proportional_command
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
- Imported get_proportional_command from guidance_logic.py
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
- Multiple plots needed to be saved without interference

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
- How can distance-aware behavior be added to the controller
- How can the UAV decide when to approach, descend, or hold position?





## Session 10 - June 21, 2026

### Accomplished
- Added marker apparent size calculation to detect_marker.py
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
- Compared detected marker size to known corner positions
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
- How can marker size commands be turned into numeric approach and descent commands?
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

### Problems
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
- How can X, Y, and Z command histories be stored and plotted?
- How can final movement outputs become the foundation for mission state logic?





## Session 13 - June 24, 2026

### Accomplished
- Created simulate_final_movement.py in Guidance
- Imported full guidance function chain
- Added controller tuning for tolerance, gain, max commands, desired size, tolerance, and approach
- Added one-step final movement command calculation
- Built a loop to simulate X, Y, and Z over time
- Updated simulated errorX, errorY, and markerSize in loop
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
- Demonstrated the full behavior sequence: center then adjust distance then maintain
- Confirmed simulation stops with both end conditions

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





## Session 15 - June 26, 2026

### Accomplished
- Added history tracking to run_movement_simulation()
- Created history lists for simulation step, X error, Y error, marker size, final X command, final Y command, final Z command, and combined command
- Stored simulation values during each loop iteration
- Updated the simulation function to return final values and history lists
- Updated the test-case call to receive the returned history values
- Confirmed that adding history tracking did not change the simulation results
- Created a position-error plot for errorX and errorY
- Created a marker-size plot
- Created a final movement command plot for xFinal, yFinal, and zFinal
- Saved all final movement plots to the Guidance folder

### Problems
- The simulation originally only returned final values, so behavior over time could not be visualized
- History lists needed to be returned from both the success case and the maximum-step case
- The function call at the bottom of the file needed to receive many more returned values
- Plotting needed to be added without changing the existing simulation behavior
- Plot code needed to stay inside the main test section so importing the function later would not automatically create plots

### Debugging
- Added history lists without changing the original final summary output
- Ran the file to confirm the printed outputs stayed the same
- Updated both return statements to include all history lists
- Updated the receiving variables in the test loop
- Ran the simulation again to confirm the summaries still worked
- Created a dedicated plotting case using a starting position and marker size that required both centering and distance adjustment
- Checked the position-error plot to confirm that X and Y errors moved into the tolerance band
- Checked the marker-size plot to confirm that marker size changed after centering
- Checked the final-command plot to confirm that X/Y commands acted first and Z command acted second
- Used plt.close() after saving plots to cleanly close each figure

### Solution
- Stored simulation history values at every step
- Returned both final values and histories from run_movement_simulation()
- Used Matplotlib to visualize position error over time
- Used Matplotlib to visualize marker-size behavior over time
- Used Matplotlib to visualize final X, Y, and Z commands over time
- Confirmed visually that the final movement simulation centers first, adjusts distance second, and stops once complete
- Saved the plots as reusable project artifacts for documentation and future analysis

### Next Session
- How can the simulation and plotting code be cleaned up for readability?
- How can repeated plot code be refactored into helper functions?
- How can the final movement simulation results be explained clearly in the README?





## Session 16 - June 28, 2026

### Accomplished
- Cleaned up repeated plotting code in simulate_final_movement.py
- Created a reusable save_plot() helper function
- Made save_plot() handle one or more plotted histories
- Added support for optional horizontal reference lines
- Used default values of None for plots that do not need horizontal lines
- Replaced the final movement command plot block with a save_plot() call
- Replaced the position-error plot block with a save_plot() call
- Replaced the marker-size plot block with a save_plot() call
- Kept all plotting code inside if __name__ == "__main__":
- Added a short comment explaining the purpose of save_plot()
- Confirmed all three plots still save correctly after refactoring

### Problems
- The plotting section had three repeated blocks of similar Matplotlib code
- The command plot did not need horizontal lines, but the error and marker-size plots did
- The helper function needed to work for both cases
- The function needed to handle multiple plotted histories, not just one
- The code needed to stay import-friendly

### Debugging
- First tested the helper function on the command plot because it did not need tolerance lines
- Confirmed the command plot still saved correctly
- Added optional horizontalLines and horizontalLabels inputs
- Used default values so plots without horizontal lines could skip those arguments
- Replaced the error plot with a helper call using positive and negative tolerance lines
- Replaced the marker-size plot with a helper call using upper and lower size tolerance lines
- Ran the simulation again and confirmed all three plots saved correctly

### Solution
- Refactored repeated plotting code into one reusable helper function
- Used a loop with zip(plottedHistories, labels) to plot multiple histories
- Used optional horizontal reference lines for tolerance bands
- Simplified the bottom of the simulation file to three short save_plot() calls
- Improved code readability and reusability without changing the simulation behavior

### Next Session
- How can the final movement simulation results be explained clearly in the README?
- How can controller behavior be summarized using the saved plots?
- How can this simulation connect to mission-state logic?





## Session 17 - June 30, 2026

### Accomplished
- Added a Final Movement Simulation section to the README
- Explained what the final movement simulation tests
- Described how X and Y position errors are used for lateral guidance
- Described how marker size is used to estimate distance from the target
- Explained the center-first guidance behavior
- Explained how the system adjusts distance after the marker is centered
- Added a Simulation Plots subsection
- Documented the purpose of the final movement error plot
- Documented the purpose of the final movement marker-size plot
- Documented the purpose of the final movement command plot
- Updated the README Completed section
- Cleaned up the README In Progress section
- Removed completed items from the Planned section

### Problems
- No new code was written during this session
- The main challenge was explaining the simulation clearly without making the README too long
- The README needed to describe what the plots prove, not just list that they exist
- The Planned and In Progress sections needed to be updated so they matched the current project status

### Debugging
- Reviewed the README structure to decide where the new section should go
- Placed the Final Movement Simulation section after the system architecture and mission state overview
- Revised the paragraph to make the wording more engineering-focused
- Changed the Simulation Plots heading into a subsection
- Changed the final plot summary from a bullet point into a normal explanatory sentence
- Fixed README status sections so completed documentation was no longer listed as in progress

### Solution
- Added a clear README explanation for the final movement simulation
- Connected the simulation behavior to UAV landing logic
- Explained that the system centers the marker first, adjusts distance second, and stops when the final condition is reached
- Documented the saved plots so someone viewing the GitHub repository can understand what they show
- Improved the README as a project presentation artifact

### Next Session
- How can combined command history be summarized?
- How can the controller behavior be explained using command modes?
- How can command summaries prepare the project for mission-state logic?





## Session 18 - July 1, 2026

### Accomplished
- Added command history summarization to `simulate_final_movement.py`
- Created `summarize_command_history()`
- Used `combinedCommandHistory` to count how many steps were spent in each command mode
- Created a command summary dictionary
- Fixed the dictionary-checking logic in the command summary function
- Printed the command summary for the dedicated plotting simulation case
- Confirmed the command summary matched the expected behavior sequence
- Added singular and plural formatting for `step` and `steps`
- Created `print_command_summary()` to clean up the main section of the file
- Refactored command summary printing into a helper function
- Confirmed the output stayed the same after refactoring

### Problems
- The first version of the command summary checked `commandHistory` instead of `commandSummary`
- This caused the dictionary count logic to fail because new commands were not being added correctly
- The command summary output initially printed raw dictionary-style output
- The main section of the file became cluttered when the print loop was written directly at the bottom
- The output needed to distinguish between `1 step` and multiple `steps`

### Debugging
- Reviewed how the command history list stores command modes like `center`, `closer`, `further`, and `maintain`
- Fixed the condition so the function checks whether each command is already in the summary dictionary
- Ran the simulation and confirmed the summary output showed `center`, `closer`, and `maintain`
- Verified that the command summary was based on the dedicated plotting simulation case
- Added a cleaner print loop for readable output
- Refactored the print loop into `print_command_summary()`
- Re-ran the simulation and confirmed the same command summary was printed

### Solution
- Added a reusable command-history summary function
- Counted how many simulation steps were spent in each command mode
- Added readable terminal output for command summaries
- Improved the simulation’s ability to explain controller behavior numerically
- Confirmed that the final movement behavior follows the expected sequence: center first, adjust distance second, then maintain

### Next Session
- How can harder final movement simulation test cases be added?
- How can command summaries be compared across multiple starting conditions?
- How can these summaries help tune the controller?





## Session 19 - July 2, 2026

### Accomplished
- Added harder final movement simulation test cases
- Replaced basic tuple-only test cases with labeled test cases
- Added readable test-case names to the simulation output
- Tested cases with large X/Y position errors
- Tested cases where the marker was too far away
- Tested cases where the marker was too close
- Tested cases where the marker was almost centered but at the wrong distance
- Tested cases where the marker was centered but still needed distance correction
- Added step-count output for each test case
- Confirmed all normal test cases reached final movement of `0 0 0`
- Identified that extremely large starting values work as stress tests but are less realistic than normal camera-based values

### Problems
- Some initial test values were extremely large compared to realistic image pixel errors
- Very large X/Y errors and marker-size values caused the simulation to take hundreds or thousands of steps
- The original test-case output was harder to understand because each case did not have a label
- Normal test cases and stress test cases needed to be treated differently

### Debugging
- Ran the harder simulation cases and checked final errors, final marker size, final movement, and steps needed
- Confirmed that each case eventually reached the final stop condition
- Compared step counts to see which starting conditions were more difficult
- Recognized that large values such as `20000`, `-30000`, or `40000` are useful stress tests but not realistic normal image conditions
- Added labels to make each test case easier to interpret in the terminal output
- Confirmed the labeled test output printed correctly

### Solution
- Improved the final movement simulation test suite with harder and more descriptive test cases
- Used labeled cases to make the output easier to understand
- Kept realistic cases focused on normal camera-like error ranges
- Treated extreme values as stress tests rather than normal expected flight conditions
- Confirmed that the final movement controller can center the marker, adjust distance, and stop across multiple starting conditions

### Next Session
- How can command summaries be compared across multiple test cases?
- How can normal and stress test cases be separated cleanly?
- How can controller parameters be tuned using step-count results?





## Session 20 - July 3, 2026

### Accomplished
- Added command summaries for every final movement test case
- Used `summarize_command_history()` inside the main test-case loop
- Used `print_command_summary()` to print readable command-mode counts
- Confirmed each test case shows how many steps were spent in each command mode
- Added test type labels to each test case
- Labeled test cases as either `normal` or `stress`
- Kept all test cases in one list to reduce repeated code
- Updated the test-case loop to read test type, test name, starting X error, starting Y error, and starting marker size
- Increased `maxSteps` so stress tests could finish
- Added clearer output labels for the final movement test cases
- Added a clearer output label for the plotting simulation
- Added a label for the plotting simulation command summary
- Confirmed normal and stress test cases reached final movement of `0 0 0`
- Confirmed plot files still save correctly

### Problems
- The output originally showed command summaries only for the dedicated plotting simulation
- The command summary needed to be printed for each test case to compare behavior across starting conditions
- Normal and stress tests were mixed together without a clear label
- Some stress cases required thousands of steps, so the previous maximum step limit could be too low
- The plotting simulation command summary could be confused with the full test suite summary

### Debugging
- Added command summary output inside the test-case loop
- Fixed duplicate `Command summary:` headings by relying on `print_command_summary()`
- Checked that command summary counts added up to the printed steps needed
- Added `normal` and `stress` labels inside the test-case tuples
- Updated the loop to unpack the test type and test name
- Increased the maximum step count to allow stress tests to finish
- Added terminal headings to separate final movement test cases from the plotting simulation
- Re-ran the file and confirmed all expected outputs printed correctly

### Solution
- Improved the final movement simulation test output so each case now shows both final results and command-mode behavior
- Kept the test structure compact with one labeled test-case list
- Made the output easier to interpret by separating normal tests from stress tests
- Confirmed the controller can center, adjust distance, and maintain across multiple test conditions
- Confirmed the simulation output now explains how the controller reached the final condition, not just that it reached it

### Next Session
- How do different controller parameter values affect step counts?
- Which controller settings are too slow or too aggressive?
- What default values should be used before moving into mission-state logic?





## Session 21 - July 4, 2026

### Accomplished
- Added controller parameter tuning to `simulate_final_movement.py`
- Created a `parameterSets` list for comparing different controller settings
- Tested the current default controller settings
- Tested a slower response parameter set
- Tested a faster response parameter set
- Tested an aggressive response parameter set
- Used the same starting condition for each tuning test
- Compared how many steps each parameter set needed to reach the final condition
- Added a `tuningResults` list to store parameter names and step counts
- Printed a compact tuning step comparison after the tuning loop
- Confirmed that every parameter set reached final movement of `0 0 0`
- Kept the current default values as the conservative baseline for now

### Problems
- The faster and aggressive parameter sets performed better in simulation, but simulation does not include real drone dynamics
- The aggressive response reached the final condition fastest, but it may be unsafe as a first hardware setting
- The tuning output needed to stay numeric and consistent with the rest of the simulation output
- A written tuning conclusion did not fit well inside the terminal output style

### Debugging
- Added multiple parameter sets and ran the same test case with each one
- Checked the final X error, Y error, marker size, final movement, and steps needed for each parameter set
- Confirmed the slower response took the most steps
- Confirmed the current default acted as a middle-ground baseline
- Confirmed the faster response reduced the step count
- Confirmed the aggressive response was fastest in simulation
- Added a compact tuning comparison to make the output easier to read
- Kept the interpretation in the session log instead of printing it directly in the program

### Solution
- Created a controller tuning comparison system
- Stored each parameter set’s step count in `tuningResults`
- Printed a compact step comparison for all tested parameter sets
- Used the results to compare conservative, slower, faster, and aggressive controller behavior
- Decided to keep the current default parameters for now because they are a safer baseline before hardware testing
- Identified the faster response as a possible future tuning option after more testing

### Next Session
- How can guidance outputs be connected to a physical command interface?
- How can `xFinal`, `yFinal`, and `zFinal` be sent to a future drone control layer?
- How can dry-run command sending prepare the project for hardware integration?





## Session 22 - July 5, 2026

### Accomplished
- Created the Control folder for future physical command logic
- Built a dry-run velocity command interface
- Added a stop command helper
- Added command limiting so unsafe command values are capped before being sent
- Connected the final movement simulation output to the command interface
- Verified that xFinal, yFinal, and zFinal can flow into a dry-run physical command output

### Problems
- Importing the command interface from the guidance simulation was not immediately straightforward
- The command interface needed to work regardless of where the project is run from

### Debugging
- Used pathlib and sys.path to add the project root to the Python path
- Tested the command interface by sending normal, stop, and oversized commands
- Confirmed oversized commands were limited to the safe command range

### Solution
- Kept the command interface in Code/Control/command_interface.py
- Used send_velocity_command() as the bridge between simulated guidance outputs and future physical UAV commands
- Verified the simulation can call send_velocity_command(xFinal, yFinal, zFinal)

### Next Session
- How can the UAV organize behavior using mission states?
- How should TAKEOFF, SEARCH, TRACK, LAND, and DISARM be represented in code?
- How can mission-state logic decide which guidance behavior should run?





## Session 23 - July 6, 2026

### Accomplished
- Created the Mission folder for mission-level UAV behavior
- Built the first mission-state update function
- Added TAKEOFF logic that keeps the UAV in TAKEOFF until the target altitude is reached
- Added transition logic from TAKEOFF to SEARCH
- Added state-based command generation
- Connected mission-state commands to the dry-run command interface
- Verified that TAKEOFF sends an upward command and SEARCH sends a stop command for now

### Problems
- The first version of the state update logic depended only on altitude
- That would have allowed non-TAKEOFF states to accidentally switch back to TAKEOFF
- String comparison needed to use == instead of is

### Debugging
- Tested TAKEOFF below target altitude
- Tested TAKEOFF at target altitude
- Tested SEARCH and LAND to make sure they stayed unchanged
- Tested mission commands for TAKEOFF, SEARCH, and LAND
- Tested the full transition from TAKEOFF to SEARCH through the command interface

### Solution
- Updated mission logic so altitude only affects the TAKEOFF state
- Kept all other states unchanged for now
- Added get_state_command() so each mission state can produce a movement command
- Verified TAKEOFF produces a dry-run upward command through send_velocity_command()

### Next Session
- How can simulated altitude change over time during TAKEOFF?
- How should the UAV decide when takeoff is complete?
- How can TAKEOFF become a reusable mission behavior instead of a single test case?





## Session 24 - July 7, 2026

### Accomplished
- Added simulated altitude update logic
- Built a takeoff simulation loop
- Connected TAKEOFF commands to simulated altitude changes
- Verified the UAV stays in TAKEOFF while below target altitude
- Verified the UAV switches to SEARCH when target altitude is reached
- Added a maxSteps safety limit to prevent infinite takeoff loops
- Added a safe stop command if takeoff fails before reaching the target altitude
- Added a takeoffComplete return flag

### Problems
- Printed altitude values initially showed floating-point rounding artifacts
- The first maxSteps safety version still sent an upward TAKEOFF command after failing to reach target altitude

### Debugging
- Rounded printed altitude values for readability without changing stored altitude
- Tested normal takeoff with enough steps to reach SEARCH
- Tested failed takeoff with too few maxSteps
- Confirmed the failed case now sends a stop command instead of another upward command

### Solution
- Added update_altitude() to simulate vertical motion from zCommand
- Added run_takeoff_simulation() to simulate autonomous takeoff behavior
- Used maxSteps to prevent runaway loops
- Returned currentState, currentAltitude, and takeoffComplete for later mission integration

### Next Session
- How can TAKEOFF connect into a larger full mission simulation?
- How should the mission move from SEARCH toward target acquisition?
- How can mission-state logic decide what behavior runs next?





## Session 25 - July 8, 2026

### Accomplished
- Expanded mission-state logic from TAKEOFF and SEARCH to include ACQUIRE
- Added marker-detection awareness to the mission-state update function
- Added SEARCH to ACQUIRE transition logic
- Updated SEARCH to produce a placeholder search command
- Built a basic full mission simulation
- Verified the mission can progress from TAKEOFF to SEARCH to ACQUIRE
- Added a failure warning when the mission stops before reaching ACQUIRE

### Problems
- The mission-state update function needed a new markerDetected input
- Existing calls to update_mission_state() had to be updated to include the new argument
- The mission needed a way to simulate marker detection before real camera integration

### Debugging
- Tested TAKEOFF below and at target altitude.
- Tested SEARCH with markerDetected set to False and True.
- Tested the full mission with marker detection occurring at step 25
- Tested a failure case where maxSteps ended before marker detection
- Confirmed the success case ends in ACQUIRE and the failure case ends in SEARCH

### Solution
- Added markerDetected to update_mission_state().
- Added SEARCH logic that switches to ACQUIRE when a marker is detected
- Added run_basic_mission_simulation() to simulate TAKEOFF, SEARCH, and ACQUIRE together
- Used markerDetectionStep as a simulated marker-detection trigger

### Next Session
- How can mission logic connect to real or simulated guidance outputs?
- How should ACQUIRE begin using marker position errors?
- How can the mission move from ACQUIRE into TRACK?





## Session 26 - July 16, 2026

### Accomplished
- Connected mission logic to the existing guidance system
- Added guidance imports to the mission-state file
- Built get_acquire_command() for ACQUIRE-state movement
- Used simulated marker error and marker size values to generate guidance commands
- Connected ACQUIRE guidance output to the dry-run command interface
- Tested off-center, too-far, too-close, and correct-size marker cases

### Problems
- get_proportional_command() needed the maxCommand argument
- ACQUIRE needed to return both final movement commands and the combined guidance command
- The first tests had to be changed manually before being converted into a reusable test-case list

### Debugging
- Tested an off-center marker to confirm ACQUIRE prioritizes centering
- Tested a centered but too-far marker to confirm the system commands closer movement
- Tested a centered but too-close marker to confirm the system commands further movement
- Tested a centered and correct-size marker to confirm the system maintains position
- Verified all final commands pass through send_velocity_command()

### Solution
- Added get_acquire_command() as the bridge between mission state and guidance logic
- Used the existing guidance chain to compute xFinal, yFinal, zFinal, and combinedCommand
- Added reusable ACQUIRE command tests for the main marker-alignment cases

### Next Session
- How can ACQUIRE transition into TRACK?
- How should the mission respond when marker alignment improves over time?
- How can simulated marker error updates be connected to mission-state transitions?





## Session 27 - July 17, 2026

### Accomplished
- Added LiDAR obstacle avoidance as a future add-on if extra time is available
- Updated the hardware plan to focus on a Pixhawk-style flight controller and laptop companion-computer architecture
- Updated the requirements document to match the new hardware and autonomy scope
- Updated the README to include the Pixhawk-style hardware direction, MAVLink command-interface planning, and future LiDAR add-on
- Cleaned and reformatted the engineering log for consistency

### Problems
- The original hardware scope was becoming too large for the remaining project timeline
- Adding LiDAR would have increased hardware complexity, wiring, code, and debugging time
- The project needed a clearer distinction between required goals and future add-ons
- The engineering log had inconsistent heading levels, spacing, and small typos
- The README, requirements file, and hardware plan needed to match the updated project direction

### Debugging
- Compared the difficulty of completing full autonomous physical flight with and without LiDAR
- Identified LiDAR as useful but not necessary for the first full autonomous flight goal
- Reworked the project scope so the main priority is TAKEOFF to LAND autonomous flight
- Reviewed the requirements file and moved LiDAR from project scope to future work
- Reviewed the README status sections and updated Completed, In Progress, and Planned items
- Reviewed the engineering log for heading consistency, typo fixes, and spacing
- Checked that every log entry uses the same section structure

### Solution
- Set the required project goal as autonomous ArUco-guided flight from takeoff toward landing
- Kept LiDAR-based obstacle avoidance as an optional future upgrade only
- Updated the hardware plan so LiDAR is not included in the first hardware order
- Updated the requirements file to include hardware safety, MAVLink communication, and physical drone testing goals
- Updated the README to show the current hardware direction and future LiDAR status
- Cleaned the engineering log and standardized all future entries to the same format
- Prepared the project to move next into exact parts selection and MAVLink planning

### Next Session
- What exact hardware parts should be ordered for the first physical drone build?
- Which Pixhawk-style flight controller or kit should be selected?
- How should the MAVLink command interface be planned before hardware arrives?





## Session 28 - July 18, 2026

### Accomplished
- Finalized the initial hardware order for the physical drone phase
- Selected the Holybro S500 V2 Development Kit with Pixhawk 6C as the main drone platform
- Selected Zeee 4S 3000mAh XT60 LiPo batteries for flight power
- Selected the ISDT 608AC charger for the drone batteries
- Selected the RadioMaster Pocket ELRS transmitter for manual control and safety override
- Selected the RadioMaster RP1 ELRS receiver for the flight controller
- Selected RadioMaster 18650 transmitter batteries from Lumenier
- Selected spare 1045 propellers for testing and replacement
- Selected a LiPo voltage checker and low-voltage alarm
- Selected a metric hex driver set for assembly and maintenance
- Selected reusable Velcro cable ties for cable management
- Selected heat shrink tubing for wiring protection
- Selected a LiPo safe charging and storage bag
- Clarified that the drone batteries charge with the ISDT charger
- Clarified that the transmitter batteries charge inside the RadioMaster Pocket through USB-C

### Problems
- Physical drone parts will not arrive before the next session
- Hardware costs are near the planned budget, so extra parts had to be limited
- Some recommended online items were not useful for this project

### Debugging
- Checked each hardware item against the project requirements
- Confirmed the battery, charger, transmitter, receiver, propeller, and safety-item choices
- Separated required first-order hardware from optional future tools
- Confirmed that a separate 18650 charger is not needed for the transmitter batteries
- Confirmed that LiDAR obstacle avoidance should remain future work

### Solution
- Completed the initial hardware order list
- Stopped adding nonessential parts
- Decided to continue software development while waiting for the hardware to arrive
- Set the next task as the ACQUIRE to TRACK transition
- Kept the early hardware safety rule that propellers will stay off during bench testing

### Next Session
- How can ACQUIRE transition into TRACK?
- How long should the marker stay centered before switching to TRACK?
- What tolerance should be used for the ACQUIRE to TRACK transition?
- How can the system avoid switching states because of one noisy detection?
- What software work can continue while waiting for hardware delivery?





## Session 29 - July 19, 2026

### Accomplished
- Added an ACQUIRE completion check to the mission-state logic
- Created is_marker_acquired() to check whether the marker is centered and at the correct apparent size
- Checked X error against the position tolerance
- Checked Y error against the position tolerance
- Checked marker size against the desired marker size and size tolerance
- Created update_acquire_stability() to track how long the marker has stayed acquired
- Added stableCount to count consecutive acquired frames
- Added requiredStableCount to define how many stable frames are needed before switching states
- Added readyToTrack as the condition for leaving ACQUIRE
- Updated update_mission_state() so ACQUIRE can transition into TRACK
- Tested the ACQUIRE completion logic with centered, off-center, too-far, and too-close marker cases
- Tested the stability counter with a sequence of acquired and not-acquired values
- Built a combined ACQUIRE to TRACK simulation using simulated marker errors and marker sizes
- Confirmed that a bad frame resets stableCount to zero
- Confirmed that the mission only switches to TRACK after three stable acquired frames

### Problems
- The first combined simulation loop tried to unpack five values from marker data that only contained four values
- The loop needed enumerate() to create the step number separately
- Several variables used in the combined simulation were not defined before the loop
- The mission needed to avoid switching from ACQUIRE to TRACK after only one good frame

### Debugging
- Checked the ACQUIRE completion test output for each marker case
- Verified that only the centered and correct-size marker case returned acquired as True
- Checked the stability test output step by step
- Verified that stableCount increased during acquired frames
- Verified that stableCount reset to zero after a bad frame
- Replaced the incorrect loop unpacking with enumerate()
- Added currentState, stableCount, requiredStableCount, and simulatedMarkerData before the combined simulation loop
- Ran the combined simulation and checked that currentState stayed ACQUIRE until readyToTrack became True
- Confirmed that currentState changed to TRACK only after stableCount reached three

### Solution
- Added a reliable ACQUIRE completion condition using position error and marker size
- Added a stability counter so one noisy detection cannot trigger the TRACK state
- Connected readyToTrack into update_mission_state()
- Confirmed the full ACQUIRE to TRACK transition using simulated marker data
- Kept the mission-state logic ready for TRACK behavior in the next session

### Next Session
- How should TRACK state behavior keep the marker centered over time?
- What commands should TRACK produce when the marker is slightly off center?
- How should TRACK respond if the marker is temporarily lost?
- How should TRACK decide when the drone is ready to move into APPROACH?
- How can TRACK behavior build on the ACQUIRE stability logic?





## Session 30 - July 21, 2026

### Accomplished
- Added TRACK state command behavior
- Created get_track_command() to keep the marker centered during TRACK
- Used errorX and errorY as inputs for TRACK correction
- Reused get_proportional_command() for TRACK X and Y movement
- Set zCommand to zero during TRACK so the drone does not approach or descend
- Tested TRACK commands with centered, right, left, low, high, and small-error marker cases
- Confirmed centered marker cases produce zero movement
- Confirmed large X and Y errors produce correction commands
- Confirmed small errors inside tolerance produce zero movement
- Connected TRACK commands to the dry-run command interface
- Added dry-run TRACK command tests using send_velocity_command()
- Built run_track_simulation() to simulate TRACK correction over time
- Simulated marker error updates using correctionScale
- Confirmed TRACK reduces X and Y errors toward zero
- Confirmed TRACK reaches the centered condition when both errors are inside tolerance

### Problems
- TRACK needed to be clearly separated from APPROACH and LAND
- TRACK needed to correct marker position without changing altitude
- The mission needed a safe default command for TRACK when marker error inputs are not available
- Floating-point command values appeared in the TRACK simulation output

### Debugging
- Tested get_track_command() with several simulated marker positions
- Verified zCommand stayed zero for every TRACK test case
- Sent TRACK command outputs through the dry-run command interface
- Checked the TRACK simulation step by step
- Verified errorX and errorY moved closer to zero after each correction
- Confirmed yCommand stopped once Y error entered the tolerance range
- Confirmed xCommand stopped once X error entered the tolerance range
- Checked the final error values against the tolerance

### Solution
- Defined TRACK as a hold-altitude marker-centering state
- Used proportional X and Y correction during TRACK
- Kept Z movement disabled during TRACK
- Added a simulation to verify TRACK can center the marker over time
- Confirmed TRACK reaches a centered condition without approach or descent
- Decided to handle lost-marker behavior in the next session
- Decided that future sessions should include more independent coding before reviewing full solutions

### Next Session
- How should TRACK respond when the marker is temporarily lost?
- How many missed detections should be allowed before leaving TRACK?
- Should TRACK stop, hold position, or return to SEARCH after marker loss?
- How can lost-marker handling be tested with simulated detection sequences?
- How can future coding sessions allow more independent implementation before debugging?





## Session 31 - July 22, 2026

### Accomplished
- Added TRACK lost-marker handling
- Created update_track_marker_loss() to count missed marker detections during TRACK
- Added lostMarkerCount to track consecutive frames without marker detection
- Added maxLostMarkerCount to define how many missed detections are allowed
- Added markerLost as the condition for leaving TRACK
- Tested marker loss counting with detected and not-detected marker sequences
- Confirmed detected frames reset lostMarkerCount to zero
- Confirmed missed frames increase lostMarkerCount
- Confirmed markerLost becomes True after three missed detections in a row
- Updated update_mission_state() so TRACK can transition back to SEARCH
- Added markerLost as an optional mission-state input
- Tested TRACK marker-loss transition behavior
- Confirmed TRACK stays TRACK when markerLost is False
- Confirmed TRACK returns to SEARCH when markerLost is True
- Built a combined marker-loss simulation
- Confirmed temporary marker loss does not immediately leave TRACK
- Confirmed TRACK returns to SEARCH after too many missed detections

### Problems
- TRACK needed a way to handle temporary marker loss without immediately leaving the state
- TRACK also needed a safety limit so the drone does not continue tracking when the marker is gone
- The first update_mission_state() edit made markerLost a required input
- The mission needed markerLost to be optional so older mission-state calls would still work

### Debugging
- Tested update_track_marker_loss() with a sequence of marker detections
- Checked that lostMarkerCount reset when markerDetected was True
- Checked that lostMarkerCount increased when markerDetected was False
- Checked that markerLost became True only after lostMarkerCount reached maxLostMarkerCount
- Changed the mission-state function signature so markerLost defaults to False
- Tested TRACK with markerLost False and markerLost True
- Ran the combined marker-loss test sequence
- Verified that currentState stayed TRACK during temporary missed detections
- Verified that currentState changed to SEARCH after three missed detections in a row

### Solution
- Added a consecutive missed-detection counter for TRACK
- Allowed short marker dropouts without immediately leaving TRACK
- Added a safety transition from TRACK back to SEARCH when the marker is lost for too long
- Connected markerLost into update_mission_state()
- Confirmed the full TRACK lost-marker behavior with a combined simulation
- Continued the more independent coding approach for this session

### Next Session
- How should TRACK decide when the marker is stable enough to move into APPROACH?
- What conditions should allow TRACK to transition into APPROACH?
- Should TRACK to APPROACH require multiple stable frames?
- How should marker size affect the decision to begin APPROACH?
- How can the transition into APPROACH be tested with simulated marker data?





## Session 32 - July 23, 2026

### Accomplished
- Added TRACK to APPROACH transition logic
- Created is_track_ready_for_approach() to check whether TRACK is centered enough to continue
- Used errorX and errorY to decide whether TRACK is ready for APPROACH
- Created update_track_stability() to count stable TRACK frames
- Added trackStableCount to track consecutive centered frames during TRACK
- Added requiredTrackStableCount to define how many stable frames are needed before APPROACH
- Added readyToApproach as the condition for leaving TRACK
- Updated update_mission_state() so TRACK can transition into APPROACH
- Kept markerLost as the highest-priority TRACK condition
- Tested TRACK readiness with off-center, almost-centered, centered, and bad-frame cases
- Confirmed off-center frames do not increase trackStableCount
- Confirmed centered frames increase trackStableCount
- Confirmed a bad frame resets trackStableCount to zero
- Confirmed readyToApproach becomes True after three stable centered frames
- Tested update_mission_state() with markerLost, readyToApproach, and normal TRACK cases
- Built a combined TRACK to APPROACH simulation
- Confirmed the mission stays in TRACK until readyToApproach becomes True
- Confirmed the mission changes from TRACK to APPROACH after three stable centered frames

### Problems
- TRACK needed a separate condition for deciding when to begin APPROACH
- The transition into APPROACH needed to avoid triggering after one good frame
- markerLost needed to remain higher priority than readyToApproach
- The mission needed to stay in TRACK during off-center and unstable marker frames

### Debugging
- Tested track readiness with simulated X and Y marker errors
- Checked that trackReady returned False when either error was outside tolerance
- Checked that trackReady returned True when both errors were inside tolerance
- Verified that trackStableCount increased only during centered frames
- Verified that trackStableCount reset after a bad frame
- Tested update_mission_state() for TRACK to SEARCH, TRACK to APPROACH, and TRACK staying TRACK
- Ran the final combined simulation step by step
- Confirmed the final state became APPROACH only after the required stable count was reached

### Solution
- Added a TRACK readiness check based on marker centering
- Added a stability counter for TRACK before APPROACH
- Connected readyToApproach into update_mission_state()
- Preserved the safety priority where marker loss sends TRACK back to SEARCH before APPROACH can happen
- Confirmed the full TRACK to APPROACH transition using simulated marker data
- Continued the independent coding approach for this session

### Next Session
- How should APPROACH move the drone into final landing position?
- How should APPROACH use marker size to estimate distance or closeness?
- How should APPROACH keep correcting X and Y error while moving closer?
- What command should APPROACH produce when the marker is centered but still far away?
- How can APPROACH behavior be tested with simulated marker data?





## Session 33 - July 24, 2026

### Accomplished
- Added APPROACH state command behavior
- Created get_approach_command() for APPROACH movement logic
- Reused get_acquire_command() to generate X, Y, and Z movement commands
- Added approachComplete as the output condition for finishing APPROACH
- Used is_marker_acquired() to decide when APPROACH is complete
- Tested APPROACH with an off-center marker
- Tested APPROACH with a centered marker that was too far away
- Tested APPROACH with a centered marker that was too close
- Tested APPROACH with a centered marker at the correct size
- Tested APPROACH with small position error inside tolerance
- Tested APPROACH with X error inside tolerance and Y error outside tolerance
- Tested lower and upper marker-size boundary cases
- Confirmed APPROACH corrects X and Y before changing distance
- Confirmed APPROACH moves closer when the marker is centered but too small
- Confirmed APPROACH moves further when the marker is centered but too large
- Confirmed approachComplete becomes True only when the marker is centered and at the correct size

### Problems
- APPROACH seemed very similar to ACQUIRE at first
- get_acquire_command() returned four values, but the first APPROACH version tried to unpack only three
- The difference between ACQUIRE and APPROACH needed to be clarified
- APPROACH needed a boolean output so the mission can later transition into LAND

### Debugging
- Compared get_approach_command() to get_acquire_command()
- Identified that get_acquire_command() returns xFinal, yFinal, zFinal, and combinedCommand
- Fixed get_approach_command() so it receives all four returned values
- Added approachComplete separately using is_marker_acquired()
- Ran APPROACH test cases with different marker positions and marker sizes
- Checked that off-center marker cases produced X and Y correction with zero Z movement
- Checked that centered too-far and too-close cases produced Z movement
- Checked that centered and correct-size cases produced zero movement and approachComplete True
- Verified the lower and upper size boundaries counted as complete

### Solution
- Defined APPROACH as the state that moves into final landing position while keeping the marker centered
- Reused the existing guidance chain for APPROACH movement
- Added approachComplete so APPROACH can later transition into LAND
- Confirmed APPROACH behavior with simulated marker data
- Kept APPROACH movement separate from the actual LAND descent state

### Next Session
- How should APPROACH decide when it is ready to transition into LAND?
- How should update_mission_state() use approachComplete?
- Should APPROACH to LAND happen immediately or require stable approachComplete frames?
- How can APPROACH to LAND be tested with simulated marker data?
- How should LAND behavior use slow descent while keeping marker alignment safe?





## Session 34 - July 26, 2026

### Accomplished
- Started hardware inventory after the physical parts arrived
- Confirmed the main Holybro S500 kit was present
- Identified the frame with pre-attached wiring
- Identified the landing rods and likely landing gear support pieces
- Identified the motor mount or arm-end plastic pieces
- Confirmed the included propellers were present
- Confirmed the hardware bags, screws, plastic pieces, and included zip ties were present
- Confirmed the four motors were present
- Confirmed four ESCs were mounted on the frame
- Confirmed the GPS standard box was present
- Confirmed the power module was present
- Confirmed the telemetry radio box was present
- Confirmed two telemetry radios, antennas, and wiring were present
- Confirmed the Pixhawk 6C flight controller was present
- Confirmed the PWM In adapter, PWM Out adapter, CAN/I2C splitter, and Pixhawk wiring bundle were present
- Confirmed the Amazon support parts were present
- Confirmed the RadioMaster Pocket controller was present
- Confirmed the RadioMaster RP1 ELRS receiver was present
- Confirmed the ISDT LiPo charger, two Zeee 4S LiPo batteries, LiPo safe bag, voltage checker, spare propellers, hex drivers, Velcro ties, and heat shrink tubing were present
- Confirmed the RadioMaster 18650 transmitter batteries from Lumenier were the only item not currently available
- Decided to keep the sealed hardware bags closed for now
- Decided not to begin frame assembly during the inventory session

### Problems
- The RadioMaster transmitter batteries were not available during the session
- Some frame rods and plastic pieces were not immediately identifiable
- The Pixhawk box included several adapters and wires that should not be connected randomly
- The physical parts will not be available during Sessions 38 through 41
- Assembly needed to wait until the build order and wiring plan are clearer

### Debugging
- Sorted the hardware into main drone kit, control parts, battery and charging parts, and tools or support items
- Identified the four frame-mounted electronics with three motor connection points as ESCs
- Separated propellers from the rest of the hardware to avoid installing them too early
- Checked the Pixhawk box contents without connecting any cables
- Confirmed that the RP1 receiver was present in the Amazon order
- Compared the physical parts to the expected initial hardware order
- Decided to leave sealed bags unopened to preserve organization
- Confirmed that no power, charging, motor testing, or assembly should happen during the inventory session

### Solution
- Completed the first hardware inventory without powering or assembling the drone
- Confirmed that the main drone kit and Amazon support parts are present
- Identified the only missing-from-session item as the Lumenier transmitter batteries
- Kept LiPo batteries stored safely
- Kept propellers separate and uninstalled
- Kept Pixhawk, GPS, receiver, telemetry radios, and wiring protected
- Decided to use upcoming hardware-access sessions for Pixhawk and wiring identification before assembly

### Next Session
- How can the Pixhawk 6C ports and adapters be identified safely?
- Which cables belong to the power module, GPS, telemetry radios, and PWM adapters?
- How should the receiver connection be planned before wiring anything?
- What parts should remain disconnected until bench testing?
- How can the hardware sessions be planned around the period without part access?





## Session 35 - July 27, 2026

### Accomplished
- Identified the main Pixhawk 6C ports
- Located POWER1, POWER2, GPS1, GPS2, CAN1, CAN2, TELEM1, TELEM2, TELEM3, USB, DSM, PPM/SBUS RC, SBUS OUT, I2C, FMU PWM OUT, and I/O PWM OUT
- Identified POWER1 as the likely power module connection
- Identified GPS1 as the likely GPS module connection
- Identified TELEM ports as the likely telemetry radio connection points
- Identified I/O PWM OUT as the likely main ESC signal output area
- Identified the power module large battery-side and frame-side connectors
- Identified the power module small cable port that matches Pixhawk POWER1
- Identified the GPS cable that fits Pixhawk GPS1
- Identified the telemetry radios, antennas, USB cable, and serial telemetry cable
- Confirmed the telemetry cable fits the Pixhawk TELEM ports
- Identified the RP1 receiver pads labeled negative, 5V, TX, and RX
- Confirmed the RP1 receiver uses a serial-style connection
- Identified the PWM In and PWM Out adapter pieces
- Created a preliminary wiring plan for power, GPS, telemetry, receiver, and ESC signal connections
- Kept all hardware unpowered and disconnected during the session

### Problems
- Several Pixhawk ports could be confused because many connectors are similar sizes
- The RP1 receiver should not be connected randomly to DSM, SBUS OUT, or PPM/SBUS RC
- The telemetry radios had multiple ports and needed to be separated into laptop-side and drone-side roles
- The PWM adapters needed to be identified before connecting ESC signal wires
- No power or assembly could happen until the wiring plan is clearer

### Debugging
- Read the Pixhawk case labels directly instead of guessing port functions
- Matched the power module small cable to the POWER1 port shape
- Matched the GPS cable to the GPS1 port shape
- Matched the telemetry serial cable to the TELEM port shape
- Checked the RP1 receiver labels before planning receiver wiring
- Separated telemetry radio wiring from receiver wiring
- Identified the likely purpose of the PWM Out adapter for ESC signal outputs
- Avoided plugging in cables just because they fit
- Confirmed that the flight battery, motors, and propellers should remain disconnected

### Solution
- Created a safe preliminary wiring map for the flight controller system
- Planned power module connection to POWER1
- Planned GPS connection to GPS1
- Planned telemetry radio connection to a TELEM port
- Planned RP1 receiver connection through a serial/UART-style port later
- Planned PWM Out adapter use for future ESC signal wiring
- Kept the drone unpowered and unassembled during wiring identification
- Updated the compressed schedule so the project targets full completion by August 15

### Next Session
- How should the LiPo batteries be checked safely before charging?
- How should the ISDT charger be used with the 4S flight batteries?
- What charging current should be used for the drone batteries?
- How should the LiPo safe bag and voltage checker be used?
- What battery rules need to be followed before connecting power to the drone?





## Session 36 - July 28, 2026

### Accomplished
- Identified the main connectors on both 4S LiPo batteries
- Confirmed each battery has a yellow XT60 main connector
- Confirmed each battery has a white 5-wire balance connector
- Used the LiPo voltage checker to check both batteries
- Measured Battery 1 at 15.3V total with cells around 3.81V
- Measured Battery 2 at 15.2V total with cells around 3.81V
- Confirmed both batteries are at safe storage voltage
- Identified the ISDT charger power input, output port, balance port, USB port, and rotary encoder
- Identified the charger battery screen with current, capacity, cell voltages, and total voltage
- Identified the charger status screen with charger voltage, power, cell/status information, and temperature
- Confirmed the correct future charging mode should be Balance Charge
- Confirmed the correct future battery type is LiPo
- Confirmed the correct future cell count is 4S
- Confirmed the correct future charge current should be 3.0A or lower
- Left both batteries uncharged because they were already at storage voltage
- Stored the batteries safely in the LiPo safe bag

### Problems
- The voltage checker had 9 pins even though the 4S battery only has a 5-wire balance connector
- The charger showed several values that needed to be interpreted before charging
- The batteries should not be charged too early because LiPos should not sit fully charged for days
- Charging settings need to be checked carefully before any future charging session

### Debugging
- Matched the black balance wire to the negative side of the voltage checker
- Used only the first 5 pins on the voltage checker for the 4S balance connector
- Compared individual cell voltages to normal LiPo storage voltage
- Interpreted the charger screen values before connecting any battery to the charger
- Separated charger input/status information from battery charging settings
- Avoided charging because the batteries were already in a healthy storage range

### Solution
- Confirmed both flight batteries are healthy and balanced
- Confirmed both batteries should remain stored instead of charged today
- Identified the charger ports and basic display information
- Established the future charging setup as LiPo, 4S, Balance Charge, 3.0A or lower, and 4.20V per cell
- Kept the drone unpowered and kept all propellers off
- Stored the batteries in the LiPo safe bag after checking them

### Next Session
- How should the frame assembly be planned before putting parts together?
- What order should the frame, arms, landing gear, motors, and electronics be installed in?
- Where should the Pixhawk, GPS, telemetry radio, receiver, and battery be placed?
- How should wires be routed before anything is powered?
- What should be assembled before the parts become unavailable?





## Session 37 - July 29, 2026

### Accomplished
- Began S500 V2 frame assembly using the online assembly guide
- Identified the difference between motor arms and landing gear pieces
- Confirmed the frame has two large center plates
- Confirmed the ESCs are attached to one of the frame plates
- Identified how the arms mount between the bottom plate and top plate
- Confirmed the triangular arm mounting patterns line up when both plates are used
- Routed ESC wires through the arm areas instead of pinching them under the mounts
- Worked through the PWM breakout step from the assembly guide
- Identified the FrSky receiver step as the equivalent physical placement step for the RP1 receiver
- Assembled as much of the frame as possible without completing powered wiring
- Left the power module, RC radio connection, battery, and most wiring for a later session
- Kept the propellers off
- Kept the drone unpowered

### Problems
- The kit did not include a printed manual
- The assembly guide was written for a Pixhawk 4 style setup instead of the Pixhawk 6C
- The arm screw holes appeared not to line up until the top and bottom plate sandwich layout was understood
- ESC wires were close to the arm mounting area and could have been pinched
- Step 4 was confusing because it involved the PWM breakout and did not clearly match the newer electronics
- The FrSky receiver step did not directly match the RP1 receiver included in the current setup

### Debugging
- Compared the physical pieces to the S500 V2 frame guide
- Checked arm orientation by matching the triangular mounting side to both frame plates
- Verified that the circular arm ends point outward for motor mounting
- Paused before forcing screws when the holes did not line up at first
- Reinterpreted Step 4 as a PWM breakout placement step instead of final Pixhawk wiring
- Separated frame assembly instructions from Pixhawk 6C wiring instructions
- Confirmed that the RP1 receiver replaces the FrSky receiver for physical placement
- Avoided powered wiring during mechanical assembly

### Solution
- Used the S500 V2 guide for mechanical frame assembly only
- Treated Pixhawk-specific wiring steps as placeholders to be adapted later for the Pixhawk 6C
- Routed ESC wires safely through the arm areas
- Completed major mechanical assembly progress without installing propellers
- Left detailed wiring for the next hardware session
- Kept the battery disconnected and the drone unpowered

### Next Session
- How should the power module be placed and routed?
- How should the POWER1 cable connect to the Pixhawk?
- How should the GPS cable be routed to GPS1?
- How should the telemetry radio cable be routed to a TELEM port?
- How should the RP1 receiver wiring be planned before soldering or connecting?
- How should the PWM and ESC signal wiring be organized before power testing?





## Session 38 - July 30, 2026

### Accomplished
- Continued final hardware-access setup before losing access to the physical drone
- Connected the power module into the main battery-to-frame power path
- Confirmed the power module acts between the LiPo battery and the frame power system
- Connected the power module small cable to Pixhawk POWER1
- Connected the GPS module to Pixhawk GPS1
- Connected the Holybro telemetry radio to Pixhawk TELEM1
- Connected the main PWM output cable to Pixhawk I/O PWM OUT MAIN
- Identified the ESC black and yellow wires as ESC signal/control wires
- Confirmed ESC signal order matters and should not be assigned only by clockwise position
- Identified that the RP1 receiver uses pads labeled negative, 5V, TX, and RX
- Confirmed the RP1 included wire colors are black, red, green, and white
- Mapped RP1-side wire colors as black to negative, red to 5V, green to TX, and white to RX
- Confirmed the RP1 antenna is already attached to the receiver board
- Determined that the RP1 receiver cannot be connected directly to Pixhawk using bare wire tips
- Identified that TELEM2 has 6 pins while the RP1 only needs 4 wires
- Determined that CTS and RTS pins are not needed for the RP1 receiver
- Identified the need for a JST-GH 1.25mm 6-pin pigtail cable for RP1 to TELEM2 wiring
- Ordered a JST-GH 1.25mm 6-pin pigtail cable for future receiver wiring
- Left the RP1 receiver disconnected until the correct cable arrives
- Kept the battery disconnected and the propellers off

### Problems
- The power module routing was confusing because the frame already had a battery-style power cable attached
- The ESC signal wires were initially confused with CAN or motor-side wires
- The correct ESC signal channel order could not be safely confirmed yet
- The RP1 receiver included bare-ended wires instead of a Pixhawk-compatible plug
- TELEM2 has 6 pins while the RP1 receiver only uses 4 wires
- The available 6-pin cables were either plug-to-plug or empty connector housings
- The empty connector housing could not be used without crimp pins and a crimping tool
- The RP1 receiver wiring could not be completed safely during this session

### Debugging
- Separated the power path from the Pixhawk signal path
- Identified the power module as the middle component between the battery and the frame
- Confirmed that the power module small cable belongs on POWER1
- Identified TELEM1 as the correct port for the Holybro telemetry radio
- Identified I/O PWM OUT MAIN as the correct Pixhawk motor-output connection area
- Separated ESC power wires from ESC signal wires
- Paused before assigning ESC signal wires to channels 1 through 4
- Compared the RP1 receiver pads to the included 4-wire lead
- Compared TELEM2 cable options and ruled out the CAN and I2C splitter
- Ruled out the empty 6-pin housing because bare wires cannot attach securely without crimp terminals
- Compared JST-GH cable options and ordered a likely correct 6-pin pigtail cable

### Solution
- Completed the safe obvious Pixhawk connections
- Left the drone unpowered and kept propellers off
- Connected POWER1, GPS1, TELEM1, and I/O PWM OUT MAIN
- Left RP1 receiver wiring incomplete until the correct pigtail cable arrives
- Planned future RP1 wiring through Pixhawk TELEM2
- Planned to use only 4 of the 6 TELEM2 wires for ground, 5V, TX, and RX
- Planned to leave CTS and RTS unused
- Preserved ESC signal order for later motor-order verification
- Shifted the next four sessions to software completion while hardware access is unavailable

### Next Session
- How should APPROACH transition into LAND?
- What conditions should decide that approach is complete?
- How should LAND continue correcting marker alignment while descending?
- What should LAND do if the marker is lost or alignment becomes unsafe?
- How should the LAND behavior be tested in simulation?





## Session 39 - July 31, 2026

### Accomplished
- Started the first software-only session after the final hardware-access setup session
- Rebalanced the next four software sessions so all remaining code work is spread evenly
- Reviewed the current mission state code before adding LAND behavior
- Fixed the TRACK readiness logic using absolute error checks
- Added approachComplete as an input to the mission state update function
- Added APPROACH state transition logic
- Tested that APPROACH stays in APPROACH when approachComplete is false
- Tested that APPROACH transitions to LAND when approachComplete is true
- Tested that APPROACH returns to SEARCH when markerLost is true
- Added LAND command behavior
- Made LAND continue using proportional x and y marker correction
- Made LAND descend slowly only when the marker is centered within tolerance
- Made LAND stop descending when the marker is outside tolerance
- Added landing completion logic based on landing altitude
- Added a landing altitude tolerance to avoid floating-point precision errors
- Tested landing completion above, at, and below the landing altitude
- Tested LAND altitude update behavior over multiple simulated steps
- Confirmed LAND stops at the landing altitude instead of overshooting because of floating-point precision

### Problems
- The mission state indentation became inconsistent when switching to two-space indentation
- The TAKEOFF else block was accidentally aligned with the main state-machine if statement
- The original TRACK readiness function could incorrectly allow some large negative errors
- The first LAND test block used values before they were initialized
- Older test cases from the previous session made the bottom of the file harder to manage
- The first landing altitude simulation printed 0.2 but did not mark landing complete because of floating-point precision

### Debugging
- Rewrote the mission state function using consistent two-space indentation
- Checked that each elif state lined up with the main TAKEOFF if statement
- Replaced the TRACK readiness logic with absolute-value x and y tolerance checks
- Reduced the main test block to only the tests needed for the current session
- Initialized tolerance, kp, maxCommand, and landCommand before the LAND tests
- Verified LAND command outputs for centered, small-error, x-error, y-error, and both-error cases
- Added an altitude tolerance inside the landing completion check
- Reran the LAND altitude update test to confirm landingComplete became true at the printed landing altitude

### Solution
- Completed APPROACH to LAND state transition logic
- Completed basic LAND movement behavior
- Confirmed LAND descends only when centered over the marker
- Confirmed LAND corrects x and y without descending when alignment is unsafe
- Added a simple altitude-based landing completion condition
- Added tolerance protection against floating-point altitude errors
- Confirmed the LAND altitude simulation reaches landingComplete correctly
- Left LAND to DISARM, DISARM behavior, and landing safety cases for the next session

### Next Session
- How should LAND transition into DISARM?
- What should the DISARM state command do?
- How should LAND respond if the marker is lost?
- What timeout should stop LAND if landing takes too long?
- How should normal landing, marker loss, and timeout cases be tested?





## Session 40 - August 1, 2026

### Accomplished
- Started the second software-only session focused on completing the end of the mission
- Added landingComplete as an input to the mission state update function
- Added LAND state transition logic
- Tested that LAND stays in LAND while landing is not complete
- Tested that LAND transitions to DISARM when landingComplete is true
- Tested that LAND returns to SEARCH when markerLost is true
- Added DISARM state logic
- Tested that DISARM remains in DISARM once reached
- Added landing timeout logic
- Added landingTimeout as an input to the mission state update function
- Tested that LAND returns to SEARCH when landingTimeout is true
- Added a helper function to detect landing timeout
- Tested timeout behavior below, at, and above the maximum landing step count
- Added DISARM command behavior through get_state_command
- Tested that DISARM sends zero x, y, and z commands
- Built a LAND to DISARM integration test
- Simulated LAND descending from altitude 1.0 to the landing altitude
- Confirmed LAND transitions to DISARM after landingComplete becomes true
- Confirmed DISARM sends zero movement commands after landing

### Problems
- LAND needed a clear final state after landing was complete
- DISARM needed to hold its state instead of falling through to the default state behavior
- LAND needed a safety condition for marker loss
- LAND needed a timeout condition so the drone would not remain in landing forever
- Some test variables needed to be declared before the integration test
- The timeout test variable could interfere with the integration test landing step counter if reused
- The LAND to DISARM integration test showed landingComplete one step after the altitude first reached the landing altitude because completion was checked before altitude was updated

### Debugging
- Added landingComplete to the mission state function header
- Added a LAND block after the APPROACH block
- Added a DISARM block after the LAND block
- Added landingTimeout to the mission state function header
- Updated the LAND block to check markerLost, landingComplete, and landingTimeout
- Added is_landing_timeout to compare landingStepCount against maxLandingSteps
- Added a DISARM case inside get_state_command
- Moved test setup variables to the top of the main test block
- Used a separate testLandingStepCount variable for timeout test cases
- Verified that LAND, DISARM, SEARCH, SEARCH, and DISARM appeared in the correct transition test order
- Verified that timeout returned false below the limit and true at or above the limit
- Verified that DISARM returned zero movement commands
- Ran a combined LAND to DISARM integration test to confirm the ending sequence

### Solution
- Completed the LAND to DISARM mission transition
- Completed DISARM state behavior
- Confirmed DISARM sends zero movement commands
- Added LAND marker-loss recovery back to SEARCH
- Added LAND timeout recovery back to SEARCH
- Confirmed the landing timeout helper works correctly
- Confirmed LAND descends while centered until the landing altitude is reached
- Confirmed the mission ending sequence reaches DISARM safely
- Left full mission simulation for the next session

### Next Session
- How should TAKEOFF, SEARCH, ACQUIRE, TRACK, APPROACH, LAND, and DISARM be connected in one simulation?
- What simulated variables are needed for a full mission run?
- How should marker detection be simulated during SEARCH?
- How should ACQUIRE and TRACK stability be simulated?
- How should the full mission simulation show state, altitude, commands, and completion flags?





## Session 41 - August 3, 2026

### Accomplished
- Started the third software-only session focused on full mission simulation
- Reviewed the completed mission state machine before building the full simulation
- Confirmed the mission state machine includes TAKEOFF, SEARCH, ACQUIRE, TRACK, APPROACH, LAND, and DISARM
- Added a new full mission simulation function
- Built the first full mission loop structure
- Confirmed the simulation started in TAKEOFF
- Added TAKEOFF altitude update behavior to the full mission simulation
- Confirmed TAKEOFF transitions to SEARCH after reaching the target altitude
- Added simulated marker detection during SEARCH
- Fixed the SEARCH marker detection block indentation
- Removed the duplicate step counter increment from the full mission loop
- Confirmed SEARCH transitions to ACQUIRE after simulated marker detection
- Added ACQUIRE stability simulation
- Confirmed ACQUIRE transitions to TRACK after the required stable count
- Added TRACK stability simulation
- Confirmed TRACK transitions to APPROACH after the required stable count
- Added APPROACH completion logic to the full mission simulation
- Confirmed APPROACH transitions to LAND when approachComplete is true
- Added LAND descent behavior to the full mission simulation
- Added LAND landingComplete and landingTimeout checks to the full mission simulation
- Confirmed LAND transitions to DISARM after reaching the landing altitude
- Added altitude clamping so the simulated landing does not go below the landing altitude
- Confirmed the full mission simulation ends at DISARM
- Confirmed the final simulated altitude ends at 0.2
- Confirmed missionComplete returns true

### Problems
- The first full mission loop repeated TAKEOFF because no state update behavior had been added yet
- The simulation repeated SEARCH because the SEARCH marker detection block was indented inside the TAKEOFF block
- The full mission loop had the step counter incremented twice
- The simulation repeated ACQUIRE before ACQUIRE stability was connected
- The simulation repeated TRACK before TRACK stability was connected
- The simulation repeated APPROACH before approachComplete was connected
- The simulation repeated LAND before LAND descent and landing completion were connected
- The first complete landing simulation reached altitude 0.0 instead of stopping at the landing altitude

### Debugging
- Added command generation and altitude updates inside the full mission loop
- Added markerDetected simulation after several SEARCH steps
- Moved the SEARCH detection block outside the TAKEOFF block
- Deleted the duplicate step increment
- Added acquireStableCount and requiredAcquireStableCount
- Used is_marker_acquired and update_acquire_stability during ACQUIRE
- Added trackStableCount and requiredTrackStableCount
- Used is_track_ready_for_approach and update_track_stability during TRACK
- Used get_approach_command during APPROACH to generate approachComplete
- Used get_land_command during LAND to generate descent commands
- Used update_altitude during LAND to simulate descending
- Used is_landing_complete and is_landing_timeout during LAND
- Added altitude clamping after LAND altitude updates
- Reran the simulation after each state connection to confirm the next transition worked

### Solution
- Completed the full autonomous mission simulation
- Connected TAKEOFF to SEARCH
- Connected SEARCH to ACQUIRE
- Connected ACQUIRE to TRACK
- Connected TRACK to APPROACH
- Connected APPROACH to LAND
- Connected LAND to DISARM
- Confirmed the full mission sequence reaches DISARM
- Confirmed the final altitude stays at the landing altitude
- Confirmed missionComplete returns true
- Left MAVLink command-interface preparation for the next session

### Next Session
- How should command_interface.py be prepared for MAVLink?
- What should the emergency stop command do?
- How should dry-run mode stay safe by default?
- What command logging should be added before hardware testing?
- How should real Pixhawk command placeholders be structured?





## Session 42 - August 3, 2026

### Accomplished
- Started the final software-only session before returning to hardware work
- Reviewed the current command interface before hardware integration preparation
- Confirmed velocity commands still default to dry-run mode
- Cleaned up command limiting logic for positive and negative command limits
- Added a command logging helper
- Updated velocity command output to use limited command values
- Tested normal velocity commands
- Tested stop command behavior
- Tested oversized command limiting
- Added an emergency stop command
- Tested that the emergency stop sends zero movement commands
- Added a dry-run vehicle connection placeholder
- Tested that the dry-run vehicle connection does not connect to a real vehicle
- Added a mission command wrapper
- Tested normal mission command output
- Tested oversized mission command limiting
- Updated mission_state.py to import send_mission_command
- Replaced mission simulation command calls with send_mission_command
- Reran the full mission simulation after command-interface integration
- Confirmed the full mission still reaches DISARM
- Fixed the final DISARM command printout in the full mission simulation
- Confirmed DISARM prints zero x, y, and z commands
- Confirmed the final simulated altitude stays at 0.2
- Confirmed missionComplete returns true
- Identified that a camera and onboard companion computer are required for full ArUco autonomy
- Added camera and companion-computer acquisition to the hardware integration plan

### Problems
- The command interface needed a cleaner structure before hardware integration
- The original command limiting logic worked but was less clear for negative values
- The mission code still called the lower-level velocity command directly
- The full mission simulation reached DISARM but initially printed the previous LAND descent command
- The DISARM command override was placed inside the LAND block where it could never run
- The project hardware list was missing the camera and companion-computer path needed for full autonomous ArUco landing
- The camera requirement creates a tighter timeline for the August 18 autonomy deadline

### Debugging
- Replaced the negative command limit check with a clearer command less than negative maxCommand condition
- Added command logging so dry-run outputs are easier to read
- Verified command limiting with oversized x, y, and z commands
- Added emergency stop as a named safety function
- Added connect_to_vehicle as a dry-run placeholder instead of making a real MAVLink connection
- Added send_mission_command as the mission-level command interface
- Updated mission_state.py so simulation commands pass through send_mission_command
- Reran the full mission simulation after command-interface changes
- Moved the DISARM zero-command override outside the LAND block
- Placed the DISARM command override after the mission state update and before printing
- Verified the final DISARM step prints xCommand, yCommand, and zCommand as zero
- Reviewed the autonomy chain and identified the missing vision hardware requirement

### Solution
- Completed the safe dry-run command-interface structure
- Added command limiting, command logging, emergency stop, vehicle connection placeholder, and mission command wrapper
- Connected mission simulation commands to the mission command wrapper
- Confirmed the full mission simulation still runs from TAKEOFF through DISARM
- Confirmed the final DISARM command output is zero movement
- Confirmed the software side is ready for hardware integration work
- Updated the remaining hardware plan to include camera and companion-computer acquisition for full autonomy
- Left physical Pixhawk, receiver, transmitter, motor, and vision hardware setup for the next hardware sessions

### Next Session
- How should the RP1 receiver be connected to TELEM2?
- What Pixhawk USB setup steps are needed first?
- How should the transmitter and receiver be configured safely?
- What camera and Raspberry Pi hardware should be acquired for full autonomy?
- How should hardware setup continue while waiting for camera parts to arrive?





## Session 43 - August 4, 2026

### Accomplished
- Connected the Pixhawk to Mission Planner over USB
- Identified the Pixhawk as initially running PX4 firmware
- Installed ArduCopter firmware for the quadcopter setup
- Reconnected to the Pixhawk after firmware installation
- Set the frame class to Quad
- Set the frame type to X
- Completed accelerometer calibration successfully
- Checked the compass page and confirmed external compass detection
- Postponed compass calibration because the USB cable was too short for safe rotation
- Checked the radio calibration page and confirmed no receiver input yet
- Set SERIAL2_PROTOCOL to 23 for future ELRS receiver input on TELEM2
- Verified SERIAL1 stayed configured for MAVLink2 telemetry
- Verified GPS serial settings were not changed
- Set SERIAL5_PROTOCOL to 2 and SERIAL5_BAUD to 921 for future Raspberry Pi MAVLink on TELEM3
- Disconnected the Pixhawk safely with LiPo disconnected and props off

### Problems
- Mission Planner initially could not find the correct COM port using Auto
- The Pixhawk was running PX4 instead of ArduCopter
- Firmware flashing initially failed because the wrong version was selected
- Compass calibration could not be completed safely because the USB cable was too short
- Radio calibration could not be completed because the RP1 receiver pigtail has not arrived yet

### Debugging
- Identified the Pixhawk USB port by unplugging and replugging the board
- Confirmed the correct port changed from COM5 after firmware flashing
- Used Mission Planner parameter search to diagnose the firmware mismatch
- Recognized PX4-specific parameters before changing frame settings
- Reflashed the board with the correct ArduCopter firmware
- Checked serial port parameters to avoid changing the GPS or telemetry radio ports
- Separated TELEM1, TELEM2, GPS1, and TELEM3 roles before future wiring

### Solution
- Successfully moved the Pixhawk setup from PX4 to ArduCopter
- Configured the vehicle as a Quad X frame
- Completed safe USB-only calibration and parameter setup
- Prepared TELEM2 for the ELRS receiver
- Prepared TELEM3 for the Raspberry Pi companion computer
- Stopped before unsafe compass calibration or powered motor testing

### Next Session
- How should the RP1 receiver pigtail be wired to TELEM2
- What parameters are needed for ELRS receiver input
- How should the transmitter and receiver be bound
- How should radio calibration be performed safely
- What needs to be checked before connecting the LiPo





## Session 44 - August 5, 2026

### Accomplished
- Continued Pixhawk hardware setup through Mission Planner
- Confirmed RadioMaster Pocket transmitter model was configured with Internal RF set to CRSF and External RF set to OFF
- Corrected RP1 receiver wiring after identifying the correct TELEM2 pin direction
- Verified RP1 receiver powered on after wiring correction
- Confirmed RP1 receiver showed a slow green blink when powered
- Used ExpressLRS Wi-Fi configuration to set a receiver binding phrase
- Set the same binding phrase on the transmitter
- Confirmed successful ExpressLRS link with solid green receiver LED and C indicator on transmitter
- Confirmed Mission Planner radio bars moved with transmitter stick input
- Completed radio calibration in Mission Planner

### Problems
- Initial RP1 wiring order contradicted the corrected TELEM2 pinout interpretation
- RP1 receiver originally had no LED and was not recognized
- Standard ExpressLRS bind mode would not trigger through repeated receiver power cycling
- BOOT pad method did not produce the expected double-blink bind mode
- Mission Planner radio bars did not move before receiver binding was completed

### Debugging
- Rechecked TELEM2 wire order using Pixhawk connector orientation
- Identified that the original wiring treated the wrong side of the connector as pin 1
- Corrected RP1 power, ground, TX, and RX wiring
- Tested receiver power using Pixhawk USB only
- Checked RP1 LED behavior after rewiring
- Attempted ExpressLRS binding through receiver power cycling
- Attempted ExpressLRS binding through the BOOT pad
- Entered ExpressLRS receiver Wi-Fi mode after standard bind attempts failed
- Configured receiver and transmitter with matching binding phrase
- Verified transmitter-to-receiver connection before calibrating radio input

### Solution
- Rewired RP1 receiver using the corrected TELEM2 pin order
- Used ExpressLRS Wi-Fi binding phrase instead of manual bind mode
- Confirmed the receiver and transmitter were linked through solid green LED and C indicator
- Completed Mission Planner radio calibration after RC input became visible

### Next Session
- How should flight modes be assigned to the transmitter?
- How should RC failsafe be configured?
- How should battery failsafe be configured?
- How can compass calibration be completed safely?
- What checks are needed before any motor testing?





## Session 45 - August 6, 2026

### Accomplished
- Reviewed remaining hardware needed for the full autonomous drone version
- Confirmed spare JST-GH pigtail cables can be used for future TELEM3 wiring
- Confirmed existing supplies including multimeter, Ethernet cable, long Pixhawk USB cable, zip ties, soldering tools, heat shrink, landing board, and black tape
- Selected Raspberry Pi 5 as the companion computer for onboard vision and MAVLink communication
- Planned to buy the Raspberry Pi, microSD card, reader, power supply, camera, camera ribbon cables, and micro-HDMI cable from Micro Center first
- Planned to order remaining drone-specific parts online
- Selected active cooling, onboard 5V USB-C buck converter, XT60 splitter, XT60 pigtail, jumper wires, standoffs, and mounting tape for the final order
- Decided to skip the downward rangefinder for the first autonomous version due to time constraints
- Decided to skip the smoke stopper as an optional safety tool
- Confirmed the remaining hardware should be enough for the full autonomous drone v1
- Created a day-by-day plan from August 6 through August 18 for finishing setup, code integration, testing, and final autonomous demonstration

### Problems
- Needed to make sure the final order did not miss any hardware required for the full autonomous run
- Some Amazon Raspberry Pi kits were expensive and did not include all needed accessories
- Camera cables and Pixhawk telemetry pigtail cables could be confused even though they are different cable types
- The rangefinder would be useful but would add extra setup time
- Needed to separate required items from optional safety or backup items

### Debugging
- Compared the existing spare 6-pin pigtails against the future TELEM3 wiring need
- Separated Raspberry Pi camera ribbon cables from Pixhawk telemetry pigtail cables
- Checked onboard Raspberry Pi power requirements against the selected 5V 5A USB-C buck converter
- Verified that the XT60 splitter and XT60 male pigtail would support the planned battery-to-buck-converter power path
- Crossed off tools and supplies already available at home
- Prioritized parts by whether they should be bought at Micro Center or ordered online
- Built a timeline that keeps safety setup before motor testing and manual flight before autonomy

### Solution
- Finalized the required hardware plan for the autonomous drone v1
- Planned to buy Raspberry Pi-specific items at Micro Center first
- Planned to order remaining drone wiring, power, and mounting parts online
- Confirmed the project can proceed without a rangefinder for the first autonomous ArUco landing version
- Set the next technical work sequence as flight modes, failsafes, compass calibration, motor checks, Pi setup, camera testing, MAVLink integration, bench autonomy, manual flight, and final autonomous demo

### Next Session
- How should flight modes be assigned to the transmitter?
- How should RC failsafe be configured?
- How should battery failsafe be configured?
- How can compass calibration be completed safely?
- What checks are needed before any motor testing?





## Session 46 - August 7, 2026

### Accomplished
- Purchased the Raspberry Pi 5 companion computer from Micro Center
- Purchased the Raspberry Pi Camera Module 3 Wide NoIR after the standard wide camera was unavailable
- Purchased the Raspberry Pi 5 camera ribbon cable
- Purchased the microSD card and microSD reader
- Purchased the Raspberry Pi USB-C power supply
- Purchased the micro-HDMI to HDMI cable
- Purchased the official Raspberry Pi case with fan and port access
- Ordered the remaining online hardware cart for onboard power, wiring, and mounting
- Confirmed the transmitter and receiver reconnected automatically through the existing ELRS binding phrase
- Added transmitter switches to extra RC channels
- Verified SA, SB, SC, SD, and SE switch outputs in Mission Planner
- Set SB as the main flight mode switch using Radio 6
- Changed `FLTMODE_CH` to 6 so ArduCopter uses SB for flight modes
- Configured Stabilize, AltHold, and Loiter flight modes
- Verified SB low selects Stabilize
- Verified SB middle selects AltHold
- Verified SB high selects Loiter
- Configured radio failsafe behavior
- Tested transmitter-loss behavior from the Flight Data screen
- Confirmed Pixhawk detected radio failsafe and disarmed safely
- Configured low battery failsafe at 14.0V
- Set low battery failsafe action to RTL
- Checked the battery monitor page
- Updated battery capacity to 3000 mAh
- Completed compass calibration
- Rebooted the Pixhawk after compass calibration
- Confirmed the EKF vibration warning cleared after the drone sat still

### Problems
- The standard Raspberry Pi Camera Module 3 Wide was unavailable at Micro Center
- The available camera was the Wide NoIR version, which is acceptable but not the preferred standard color version
- The transmitter switches were not originally mapped to useful extra channels
- Moving SB to Radio 5 did not produce three usable switch positions
- The first radio failsafe test on the Radio Calibration page did not clearly prove failsafe behavior
- USB-only setup caused an expected battery low voltage failsafe warning because no LiPo was connected
- GPS no fix warning remained because the setup was indoors

### Debugging
- Checked the Micro Center camera label and confirmed it was the Wide NoIR version
- Decided to use the Wide NoIR camera because it should still work for high-contrast ArUco marker detection
- Checked the Mission Planner radio bars while flipping transmitter switches
- Identified SB and SC as three-position switches
- Tried to use SB on Radio 5 but found it only produced two useful values there
- Changed ArduCopter `FLTMODE_CH` to 6 instead of forcing SB onto Radio 5
- Verified SB correctly selected flight mode slots 1, 4, and 6
- Set unused flight mode slots to safe nearby modes
- Tested transmitter loss from the Flight Data screen instead of only using the Radio Calibration page
- Confirmed radio failsafe appeared as an active Pixhawk response
- Checked battery monitor values and confirmed near-zero voltage was expected with no LiPo connected
- Completed compass calibration and waited for the vibration warning to clear

### Solution
- Used the available Raspberry Pi Camera Module 3 Wide NoIR for the first autonomous vision setup
- Completed the remaining hardware purchase and online order
- Set SB on Radio 6 as the flight mode switch
- Configured `FLTMODE_CH = 6`
- Set SB low to Stabilize, SB middle to AltHold, and SB high to Loiter
- Confirmed RC failsafe works by turning off the transmitter and observing radio failsafe disarming
- Set the low battery failsafe to 14.0V with RTL as the action
- Confirmed the battery monitor is configured for analog voltage and current on the Pixhawk 6C
- Completed compass calibration successfully
- Stopped before motor testing to keep the setup sequence safe

### Next Session
- How can the real LiPo voltage reading be checked safely?
- How can GPS lock be verified outdoors?
- How can telemetry radio connection be checked?
- What pre-motor safety checks are needed before connecting LiPo power?
- How can motor order and motor direction be verified with props removed?





## Session 47 - August 8, 2026

### Accomplished
- Checked the 4S LiPo voltage before connecting it to the drone
- Confirmed the battery was at 15.3V before testing
- Connected the LiPo with props removed, transmitter on, and Mission Planner connected
- Verified Mission Planner read the battery voltage as 15.04V
- Confirmed powered electronics current draw was about 1.02A with motors off
- Confirmed the battery low warning disappeared when the LiPo was connected
- Verified GPS outdoors
- Confirmed GPS reached 3D fix
- Confirmed GPS had 12 satellites
- Confirmed GPS HDOP was 1.1
- Confirmed the Mission Planner map position was correct outdoors
- Verified telemetry radio connection at 57600 baud
- Confirmed Mission Planner could connect through telemetry instead of Pixhawk USB
- Found and used the Pixhawk safety switch for motor testing
- Connected ESC signal and ground wires to the PWM output adapter
- Corrected the PWM adapter wiring after identifying that pin 1 was on the right side
- Confirmed all motors respond to Mission Planner Motor Test
- Tested motor order with props removed
- Corrected motor output order for Quad X
- Verified Motor Test A spins the front right motor
- Verified Motor Test B spins the back right motor
- Verified Motor Test C spins the back left motor
- Verified Motor Test D spins the front left motor
- Tested motor spin direction with props removed
- Reversed the incorrect motors by swapping two of the three motor wires
- Verified the final motor direction pattern as counterclockwise, clockwise, counterclockwise, clockwise
- Confirmed no motors or ESCs were warm after testing

### Problems
- Motor Test was initially denied by hardware because the safety switch had not been enabled
- The safety switch location was not immediately clear
- The motors initially beeped but did not spin because the ESC signal wires were not connected correctly
- The ESC yellow and black signal wires were confused with the unused receiver pigtail wires
- The PWM adapter pin orientation was initially reversed
- The first motor order test did not match the expected Quad X order
- All motors initially spun counterclockwise, so two motors needed to be reversed

### Debugging
- Identified that the unused yellow and black receiver pigtail wires should remain disconnected
- Identified that the yellow and black wires coming from the ESCs are required signal and ground wires
- Connected the ESC signal wires to the PWM output adapter
- Tested Motor Test A at low throttle values before increasing to 10 percent
- Stopped testing when the motors only beeped and did not spin
- Rechecked the PWM adapter orientation and corrected the pin direction
- Retested all four motor outputs after correcting the wiring
- Compared the tested motor order against the expected Quad X motor order
- Moved ESC signal plugs until A, B, C, and D matched the correct physical motors
- Checked motor direction from above the drone
- Reversed the back right and front left motors by swapping two thick motor wires on each motor
- Retested motor direction after the wire swaps
- Checked motor and ESC temperature after testing

### Solution
- Verified the Pixhawk battery monitor works with the real LiPo connected
- Verified GPS lock outdoors with a strong satellite count and low HDOP
- Verified telemetry radio communication through Mission Planner
- Corrected ESC signal wiring and PWM adapter orientation
- Confirmed all motors respond correctly to Mission Planner Motor Test
- Corrected the motor order for Quad X
- Corrected the motor spin direction pattern for Quad X
- Stopped before installing props or attempting any flight testing

### Next Session
- What final wiring and frame checks are needed before props are installed?
- How should prop orientation be confirmed before first flight?
- What should the full preflight checklist include?
- How should the first manual hover test be performed safely?
- What conditions must be met before testing AltHold or Loiter?





## Session 48 - August 9, 2026

### Accomplished
- Performed final preflight inspection before first hover testing
- Confirmed propeller areas were clear
- Confirmed wires were strapped down and away from motors and propellers
- Powered the drone with the LiPo for preflight checks
- Confirmed the only indoor preflight issue was the expected GPS no-fix warning
- Took the drone outside for GPS and pre-arm checking
- Confirmed outdoor preflight status was acceptable
- Cleared the hardware safety switch warning with the Pixhawk safety button
- Reviewed the correct motor direction and propeller direction layout
- Identified that the propeller thread directions did not initially match the expected diagonal motor direction pattern
- Corrected the motor and propeller arrangement so all propellers matched the correct motor directions
- Confirmed the final propeller layout matched the motor spin directions
- Armed the drone successfully
- Completed the first manual hover test in Stabilize mode
- Completed four successful Stabilize hover tests
- Verified throttle up and throttle down response
- Verified yaw left and yaw right response
- Verified pitch forward and pitch backward response
- Verified the drone armed and disarmed as expected
- Observed slight back-left drift during hover
- Confirmed first manual flight testing was successful

### Problems
- The propeller thread layout did not initially match the required motor direction layout
- The gray and black threaded propellers only fit certain motors before the motor and propeller arrangement was corrected
- The drone showed a slight back-left drift during Stabilize hover
- There was not enough time to continue into AltHold or Loiter testing
- First flight testing needed to stay conservative and avoid rushing into more advanced modes

### Debugging
- Checked that the propeller areas were clear before any powered test
- Verified that wires were secured and could not reach the propeller paths
- Checked Mission Planner pre-arm messages before flight
- Confirmed the GPS/pre-arm state outdoors before installing or using props
- Compared the motor spin directions against the propeller thread directions
- Corrected the propeller and motor arrangement before attempting flight
- Used Stabilize mode for the first hover instead of AltHold or Loiter
- Tested basic control response during hover
- Confirmed the drone responded correctly to throttle, yaw, and pitch inputs
- Treated the slight back-left drift as minor because Stabilize mode does not hold position automatically
- Stopped after successful Stabilize testing instead of moving into additional flight modes

### Solution
- Completed the first safe manual flight test sequence
- Confirmed the drone can arm, hover, respond to pilot inputs, land, and disarm
- Verified four successful Stabilize hover tests
- Kept the testing conservative and stopped before AltHold or Loiter
- Set the next step as post-flight inspection followed by controlled AltHold and Loiter testing

### Next Session
- What should be checked during the post-flight inspection?
- How should a short Stabilize confirmation hover be repeated?
- How should AltHold be tested safely for the first time?
- What GPS and wind conditions are needed before testing Loiter?
- When should the project shift back to Raspberry Pi setup and camera testing?





## Session 49 - August 10, 2026

### Accomplished
- Performed post-flight inspection after the first manual hover session
- Checked the propeller condition after a minor tip-over
- Confirmed the frame, wiring, and mounts remained secure
- Checked battery voltages before flight testing
- Used the unused 15.3V battery for additional testing
- Repeated Stabilize hover successfully
- Tested AltHold hover successfully
- Confirmed AltHold felt stable and similar to Stabilize
- Tested Loiter successfully
- Confirmed Loiter maintained position well
- Continued hover testing with manual stick inputs
- Verified pitch forward response
- Verified pitch backward response
- Verified roll left response
- Verified roll right response
- Confirmed manual control inputs behaved as expected during hover
- Verified Stabilize, AltHold, and Loiter are all working flight modes
- Prepared the Raspberry Pi hardware for software setup
- Installed the Raspberry Pi 5 into the official case
- Inserted the microSD card into the Raspberry Pi
- Finished assembling the Raspberry Pi case with the Pi and SD card installed

### Problems
- One propeller was scratched after the drone tipped over once
- The used battery from the previous flight session was lower than the unused battery
- Additional flight testing needed to stay conservative to avoid unnecessary risk
- Raspberry Pi setup could not be fully completed today
- The Raspberry Pi case needed the microSD card inserted before final assembly

### Debugging
- Compared the scratched propeller condition against the previous successful flight behavior
- Chose the higher-voltage 15.3V battery for safer test margin
- Repeated Stabilize first before moving to other modes
- Tested AltHold only after Stabilize remained stable
- Tested Loiter only after AltHold worked correctly
- Confirmed Loiter held position before trying small directional inputs
- Verified forward, backward, left, and right stick inputs during hover
- Stopped before testing RTL, transmitter-loss failsafe in air, or autonomous behavior
- Prepared the Raspberry Pi mechanically before starting software setup

### Solution
- Confirmed the drone can fly in Stabilize, AltHold, and Loiter
- Confirmed Loiter position hold works well enough for future autonomous testing support
- Confirmed basic manual directional control works during hover
- Finished the safe outdoor flight testing needed before returning to companion-computer setup
- Completed Raspberry Pi case and SD card assembly
- Set the next session as Raspberry Pi boot, camera setup, and software dependency installation

### Next Session
- How should the Raspberry Pi first boot be checked?
- How can SSH access be verified?
- How should the Raspberry Pi camera be connected and tested?
- Which Python packages are needed for ArUco detection on the Raspberry Pi?
- How can the existing vision code be moved onto the Raspberry Pi?





## Session 50 - August 11, 2026

### Accomplished
- Booted the Raspberry Pi successfully
- Confirmed the Raspberry Pi desktop loaded correctly
- Connected the Raspberry Pi to a monitor, mouse, and keyboard
- Opened the Raspberry Pi terminal
- Checked the Raspberry Pi hostname and user setup
- Fixed the internet connection after an initial name resolution issue
- Ran the Raspberry Pi package update
- Completed the Raspberry Pi full system upgrade
- Rebooted the Raspberry Pi after updates
- Installed camera and OpenCV-related packages
- Confirmed the rpicam camera tools worked
- Connected the Raspberry Pi Camera Module 3 Wide NoIR
- Left the Argon NEO 5 NVMe top plate off to avoid pinching the camera ribbon cable
- Captured a still image with the Raspberry Pi camera
- Confirmed Python could access the camera through Picamera2
- Confirmed OpenCV worked on the Raspberry Pi
- Confirmed the OpenCV ArUco module was available
- Created and ran a Raspberry Pi ArUco detection test
- Detected ArUco marker ID 0
- Confirmed the saved detection image showed a marker outline
- Created and ran a live ArUco error test
- Verified marker left movement produced negative error_x
- Verified marker right movement produced positive error_x
- Verified marker upward movement produced negative error_y
- Verified marker downward movement produced positive error_y
- Confirmed the Raspberry Pi vision system is working

### Problems
- The Raspberry Pi initially had a temporary failure in name resolution
- Copying code directly on the Raspberry Pi monitor would have taken too long
- The Argon NEO 5 NVMe top plate did not fit cleanly with the camera ribbon cable installed
- The live marker test sometimes lost detection when the marker moved too quickly or was not held flat
- There was not enough time to create the cleaner tracker script

### Debugging
- Used the Raspberry Pi desktop network connection to restore internet access
- Switched to SSH from the laptop to make copying code onto the Raspberry Pi faster
- Left the case top plate off instead of forcing it over the camera ribbon cable
- Checked still camera capture before testing Python camera capture
- Checked Python imports before running ArUco detection
- Used a still ArUco test before running a live error test
- Compared marker position with printed error_x and error_y values
- Repeated the live marker movement test more slowly to confirm consistent error signs

### Solution
- Confirmed the Raspberry Pi can boot, update, and run Python camera code
- Confirmed the Raspberry Pi camera works through both rpicam tools and Picamera2
- Confirmed OpenCV and ArUco detection work directly on the Raspberry Pi
- Verified the marker error sign convention needed for autonomous landing
- Kept the Raspberry Pi disconnected from the drone for safe setup
- Left the camera connected with the top plate off to avoid cable damage
- Set the next session to finish the clean tracker script and begin preparing for project-code and MAVLink integration

### Next Session
- How should the clean Raspberry Pi ArUco tracker script be created?
- How should detected, marker ID, error_x, and error_y be printed for the autonomy code?
- How should the project repository be cloned or copied onto the Raspberry Pi?
- How should the Raspberry Pi test scripts be organized in the project folders?
- How should the Raspberry Pi connect to the Pixhawk for the first MAVLink heartbeat test?