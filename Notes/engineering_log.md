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
- How should the UAV respond when a target is offset from the center
- How does this relate to a proportional controller?
