# Changelog

All notable changes to Fallout76CreateCustomIni are documented here.

---

## [Latest] - 2025-10-23 - GUI Version Release

### Added
- **Complete GUI Application** (`createCustomIniGUI.py`)
  - User-friendly graphical interface for non-CLI users
  - Browse buttons for easy folder/file selection
  - Real-time path validation with visual indicators (✓/✗)
  - Mod scanning and preview functionality
  - Threading to prevent GUI freezing during operations

- **Enhanced GUI Features**
  - **Mod Preview Tree**: Hierarchical view showing which mods go in which INI section
  - **Real-time Mod Counter**: Live count of detected .ba2 mods
  - **Dark Mode Toggle**: Switch between light and dark themes
  - **Settings Persistence**: Save/load folder paths and preferences to JSON file
  - **Drag & Drop Support**: Drag folders directly onto input fields (requires tkinterdnd2)
  - **Open Output Folder**: Quick access button to created INI file location
  - **Tabbed Interface**: Separate tabs for "Mod Preview" and "Output Log"
  - **Auto-detection**: Same smart path detection as CLI version

### Technical Details
- Built with tkinter (included with Python)
- Optional tkinterdnd2 for drag and drop (graceful fallback if not installed)
- Settings stored in `createCustomIni_settings.json`
- Threaded operations for responsive UI
- Cross-platform compatible (Windows, macOS, Linux)

---

## [Previous] - 2025-10-23 - Documentation Overhaul

### Changed
- **Complete README.md Rewrite**
  - Restructured with clearer sections and professional layout
  - Added comprehensive "Quick Start" guide for new users
  - Expanded "Key Features" section with detailed subsections
  - Added "Usage Examples" with practical command-line scenarios
  - New "How It Works" section explaining the process flow
  - Enhanced "Troubleshooting" section with common issues and solutions
  - Added "Technical Details" section for developers
  - Improved formatting with better use of code blocks and lists
  - More user-friendly language and organization throughout

---

## [Previous] - 2025 - Major Overhaul: Smart Detection & Robustness

### Added
- **Smart Path Detection System**
  - `find_fallout76_directory()` function automatically locates Fallout 76 directory
  - Multi-location search algorithm checks common installation paths
  - Console feedback showing which directory was detected/used

- **Comprehensive OneDrive Support**
  - OneDrive Personal (`OneDrive\Documents\My Games\Fallout 76`)
  - OneDrive Business (`OneDrive - Business\Documents\My Games\Fallout 76`)
  - OneDrive with redirected Documents folder
  - Alternative OneDrive path structures
  - Automatic fallback to standard Documents location

- **Enhanced Error Handling**
  - Data folder existence validation before processing
  - Permission error detection with `--runasadmin` suggestion
  - Import file validation before reading
  - Comprehensive try-catch blocks with descriptive messages
  - Graceful error handling with appropriate exit codes

- **Improved User Experience**
  - Progress feedback during mod scanning
  - File creation status confirmation
  - Success messages with file paths
  - Warning messages for missing import files
  - Clear, actionable error messages

### Changed
- **File Encoding**: Explicit UTF-8 encoding for all file operations
  - Supports international characters in mod names
  - Prevents encoding-related crashes

- **Error Messages**: More descriptive and actionable
  - Specific suggestions for common issues
  - Clear indication of what went wrong and how to fix it

### Fixed
- Permission issues when writing to protected directories
- Crashes when data folder doesn't exist
- Encoding errors with non-ASCII characters in mod names
- Missing import file handling

---

## [Previous] - Code Quality & Formatting Improvements

### Changed
- **Code Style Standardization**
  - Reformatted docstrings for consistency
  - Replaced single quotes with double quotes throughout
  - Improved overall code readability

- **Argument Parser Refactoring**
  - Renamed parser variable to lowercase for PEP 8 compliance
  - Enhanced argument descriptions and help texts
  - Reorganized argument definitions for better readability

- **Variable Naming Conventions**
  - Consistent naming style across the codebase
  - Changed `IMPORT_INI` to `import_ini` for consistency
  - More descriptive variable names

- **Loop and Logic Optimization**
  - Reorganized loop structures for clarity
  - Simplified list comprehensions
  - More pythonic string concatenation methods

- **File Handling Improvements**
  - Consistent use of `with open` context managers
  - Enhanced INI file writing logic
  - Removed leading comma issues in generated output

### Removed
- Unused imports (`errno`, `walk`)
- Redundant code blocks and comments
- Unnecessary complexity in file operations

### Technical Debt
- Consolidated code blocks for better efficiency
- Improved maintainability through cleaner structure
- Better separation of concerns

---

## Format

This changelog follows [Keep a Changelog](https://keepachangelog.com/) principles:
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for bug fixes
- **Security** for vulnerability fixes
