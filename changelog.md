# Changelog

## Latest Updates - Smart Path Detection & Robustness Improvements

### Path Detection Enhancement
- **Smart Directory Finding**: Added `find_fallout76_directory()` function that automatically detects Fallout 76 directory location
- **OneDrive Support**: Now supports multiple OneDrive configurations:
  - OneDrive Personal (`OneDrive\Documents\My Games\Fallout 76`)
  - OneDrive Business (`OneDrive - Business\Documents\My Games\Fallout 76`) 
  - OneDrive with redirected Documents folder
  - Standard Documents location as fallback
- **User Feedback**: Added console output showing which directory was found/used

### Error Handling & Robustness
- **Input Validation**: Added validation to check if data folder exists before processing
- **Permission Handling**: Better error messages for permission issues with suggestion to use `--runasadmin`
- **UTF-8 Encoding**: Explicit UTF-8 encoding for file operations to handle international characters
- **Import File Validation**: Check if import file exists before attempting to read it
- **Graceful Error Handling**: Comprehensive try-catch blocks with informative error messages

### User Experience Improvements
- **Progress Feedback**: Added console output showing scan progress and file creation status
- **Better Error Messages**: More descriptive error messages with actionable suggestions
- **Success Confirmation**: Clear confirmation when ini file is successfully created

---

## Previous Updates - Formatting and Styling
- Reformatted docstring for consistency.
- Replaced single quotes with double quotes for string literals.
- Improved readability by reorganizing the argument parser setup.

## Argument Parsing
- Renamed the parser variable to lowercase (`parser`).
- Enhanced descriptions and help texts for the arguments.
- Reformatted the addition of arguments for better readability.

## Removed Unused Imports
- Removed `errno` and `walk` imports which were not used.

## Variable Naming
- Changed variable names to follow a more consistent style (e.g., `IMPORT_INI` to `import_ini`).

## Logic and Loop Adjustments
- Reorganized the loop structure to enhance readability.
- Simplified list comprehensions and conditions.
- Used a more pythonic way to concatenate strings.

## File Handling
- Improved file opening logic using `with open` context managers.
- Enhanced the logic for writing to the INI file, ensuring no leading commas.

## General Code Cleanup
- Removed redundant lines and comments.
- Consolidated code blocks where possible for better efficiency.
