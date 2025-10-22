![](https://staticdelivery.nexusmods.com/mods/2590/images/314/314-1558456148-714359290.png)

# Fallout 76 Custom INI Creator

Automatically generates `Fallout76Custom.ini` files for .ba2 mod management with intelligent path detection and robust error handling.

## About

This tool scans your Fallout 76 data directory and creates a properly formatted Custom.ini file that loads all installed .ba2 mods. Originally created by GrimTech and maintained with regular updates alongside Fallout 76 patches.

**Nexus Mods**: [Fallout76CreateCustomIni](https://www.nexusmods.com/fallout76/mods/314)

## Quick Start

### GUI Version (Recommended for Beginners)
1. **Backup** your existing `Fallout76Custom.ini` (if you have one)
2. **Copy** `createCustomIniGUI.py` to your `Fallout76\Data` directory
3. **Run**: `py createCustomIniGUI.py`
4. **Use the interface** to browse folders, scan mods, and create your INI
5. **Verify** the generated file using the "Open Output Folder" button

### CLI Version (For Advanced Users)
1. **Backup** your existing `Fallout76Custom.ini` (if you have one)
2. **Copy** `createCustomIni.py` or `createCustomIni.exe` to your `Fallout76\Data` directory
3. **Run** the script:
   - Python: `py createCustomIni.py`
   - Executable: `createCustomIni.exe`
4. **Verify** the generated `Fallout76Custom.ini` in your Documents folder

Both versions automatically detect your Fallout 76 directory, including OneDrive locations.

## Versions Available

### GUI Version (`createCustomIniGUI.py`) - NEW!
Perfect for users who prefer a graphical interface:
- **Visual Interface**: Browse folders with buttons, no typing needed
- **Mod Preview**: See exactly which mods will be included before creating
- **Real-time Validation**: Visual indicators show if paths are valid
- **Dark Mode**: Toggle between light and dark themes
- **Settings Memory**: Saves your preferences for next time
- **Drag & Drop**: Drag folders directly onto input fields (optional)
- **One-Click Access**: Open output folder button after creation

See [GUI_README.md](GUI_README.md) for detailed GUI documentation.

### CLI Version (`createCustomIni.py`)
Traditional command-line interface for power users:
- **Fast Execution**: Quick command-line operation
- **Scriptable**: Easy to integrate into batch files or automation
- **Lightweight**: No GUI dependencies
- **Full Control**: All options available via command-line flags

## Key Features

### Smart Path Detection
- Automatically locates your Fallout 76 directory across multiple possible locations
- No manual configuration needed in most cases

### OneDrive Support
Seamlessly handles various OneDrive configurations:
- OneDrive Personal
- OneDrive Business
- OneDrive with redirected Documents folders
- Standard Documents folder as fallback

### Intelligent Mod Organization
Automatically categorizes mods into the correct INI sections:
- `sResourceStartUpArchiveList` - Startup mods (BakaFile, IconTag, etc.)
- `sResourceArchiveList2` - Core gameplay mods
- `sResourceIndexFileList` - Texture and map mods
- `sResourceArchive2List` - General mods (default category)

### Robust Error Handling
- Validates data folder existence before processing
- Clear error messages with actionable solutions
- UTF-8 encoding support for international characters
- Permission issue detection with admin mode suggestion

## Command Line Options

```
--datafolder <path>       Specify Fallout 76's data folder location
                          Default: current directory

--inifolder <path>        Specify where Fallout76Custom.ini should be created
                          Default: Auto-detected from Documents or OneDrive

--inifilename <name>      Specify the INI filename
                          Default: Fallout76Custom.ini

--runasadmin              Run with administrator privileges
                          Use when Fallout 76 is in a UAC-protected location

--copyinicontents <file>  Import contents from another INI file
                          Useful for preserving custom settings

-h, --help                Show help message
```

## Usage Examples

### GUI Version
```bash
# Launch the GUI
py createCustomIniGUI.py

# Then use the interface to:
# 1. Browse to your data folder
# 2. Click "Scan Mods" to preview
# 3. Click "Create Custom INI"
# 4. Click "Open Output Folder" to view result
```

### CLI Version

#### Basic Usage
```bash
py createCustomIni.py
```

#### Custom Data Folder
```bash
py createCustomIni.py --datafolder "C:\Games\Fallout76\Data"
```

#### Custom INI Location
```bash
py createCustomIni.py --inifolder "D:\MyConfigs"
```

#### Run as Administrator
```bash
py createCustomIni.py --runasadmin
```

#### Import Existing Settings
```bash
py createCustomIni.py --copyinicontents "backup.ini"
```

## How It Works

1. **Detection**: Scans multiple possible Fallout 76 directory locations
2. **Scanning**: Identifies all .ba2 files in the data folder (excluding official "SeventySix" files)
3. **Categorization**: Sorts mods into appropriate INI sections based on type
4. **Generation**: Creates a properly formatted Fallout76Custom.ini file
5. **Validation**: Confirms successful creation with console feedback

## Troubleshooting

### Permission Denied Error
If you see a permission error, try running with `--runasadmin`:
```bash
py createCustomIni.py --runasadmin
```

### Data Folder Not Found
Manually specify your data folder location:
```bash
py createCustomIni.py --datafolder "C:\Path\To\Fallout76\Data"
```

### INI File Not Created
Check that you have write permissions to your Documents folder and that the path exists.

## Technical Details

### CLI Version
- **Language**: Python 3
- **Encoding**: UTF-8 (supports international characters)
- **Compiled Version**: Built with PyInstaller for standalone execution
- **Platform**: Windows (primary), cross-platform compatible

### GUI Version
- **Language**: Python 3 with tkinter
- **Dependencies**: 
  - tkinter (included with Python)
  - tkinterdnd2 (optional, for drag & drop)
- **Settings Storage**: JSON file (`createCustomIni_settings.json`)
- **Platform**: Cross-platform (Windows, macOS, Linux)

## Installation

### Basic (Both Versions)
No installation needed - Python 3 is the only requirement.

### GUI with Drag & Drop (Optional)
```bash
pip install tkinterdnd2
```

## Notes

- The script excludes official Bethesda archives (files starting with "SeventySix")
- Mods are automatically sorted with `HUDModLoader.ba2` placed last when present
- The tool creates necessary directories if they don't exist
- Console output shows progress and confirms successful creation

## Files in This Repository

- `createCustomIni.py` - Original CLI version
- `createCustomIniGUI.py` - New GUI version with enhanced features
- `GUI_README.md` - Detailed documentation for GUI version
- `requirements-gui.txt` - Optional dependencies for GUI
- `README.md` - This file
- `changelog.md` - Version history and changes

## Contributing

This is a community tool maintained for Fallout 76 modders. Feel free to report issues or suggest improvements on the Nexus Mods page.

## Disclaimer

*"I don't normally do python.. or windows... so sorry..."* - Original Author

Despite the humble disclaimer, this tool has proven reliable for hundreds of Fallout 76 modders!
