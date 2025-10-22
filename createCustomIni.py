"""
This module creates a fallout76Custom.ini file from the installed mods in the data directory
"""

import argparse
import ctypes
import os
import sys

# Set the default filename
FILENAME = "Fallout76Custom.ini"


def find_fallout76_directory():
    """
    Find the Fallout 76 directory by checking multiple possible locations.
    Returns the path if found, otherwise returns the default path.
    """
    user_home = os.path.expanduser("~")

    # Possible locations to check (in order of preference)
    possible_paths = [
        # OneDrive Documents location
        os.path.join(user_home, "OneDrive", "Documents", "My Games", "Fallout 76"),
        # Standard Documents location
        os.path.join(user_home, "Documents", "My Games", "Fallout 76"),
        # Alternative OneDrive path structure
        os.path.join(
            user_home, "OneDrive - Personal", "Documents", "My Games", "Fallout 76"
        ),
        # Check if OneDrive redirected the entire Documents folder
        os.path.join(user_home, "OneDrive", "My Games", "Fallout 76"),
        # Business OneDrive
        os.path.join(
            user_home, "OneDrive - Business", "Documents", "My Games", "Fallout 76"
        ),
    ]

    # Check each possible path
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found Fallout 76 directory at: {path}")
            return path

    # If none found, return the standard path (will be created if needed)
    default_path = os.path.join(user_home, "Documents", "My Games", "Fallout 76")
    print(f"Using default Fallout 76 directory: {default_path}")
    return default_path


# Set the default home directory using the finder function
HOME_DIR = find_fallout76_directory()

# Get arguments from the user
parser = argparse.ArgumentParser(
    description="This program will automatically create the "
    "Fallout76Custom.ini file for you. In most cases the "
    "default arguments will be fine."
)
parser.add_argument(
    "--datafolder",
    default=".",
    help="Specify Fallout 76's data folder location (Default: current directory)",
)
parser.add_argument(
    "--inifolder",
    default=HOME_DIR,
    help="Specify the folder where Fallout76Custom.ini lives (Default: {})".format(
        HOME_DIR
    ),
)
parser.add_argument(
    "--inifilename",
    default=FILENAME,
    help="Specify the filename for the ini (Default: {})".format(FILENAME),
)
parser.add_argument(
    "--runasadmin",
    action="store_true",
    help="Runs as an admin. Use when Fallout 76 is installed in UAC location.",
)
parser.add_argument(
    "--copyinicontents", help="Copy a file's contents into your custom .ini"
)

args = parser.parse_args()

# Assign arguments to variables
mods_dir = args.datafolder
filename = args.inifilename
ini_file_path = os.path.join(args.inifolder, filename)
is_admin = args.runasadmin
import_ini = args.copyinicontents

# Configuration arrays, these are mods that should go in specific
# lists, all other go in sResourceArchive2List
RESOURCE_MAP = [
    {
        "filename": "sResourceStartUpArchiveList",
        "mods": [
            "BakaFile - Main.ba2",
            "IconTag.ba2",
            "IconSortingRatmonkeys.ba2",
            "MMM - Country Roads.ba2",
            "ImpUlt.ba2",
            "Quizzless Apalachia.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceArchiveList2",
        "mods": [
            "PerkLoadoutManager.ba2",
            "IUMesh.ba2",
            "MoreWhereThatCameFrom.ba2",
            "Prismatic_Lasers_76_Lightblue.ba2",
            "OptimizedSonar.ba2",
            "Silentchameleon.ba2",
            "CleanPip.ba2",
            "classicFOmus_76.ba2",
            "nootnoot.ba2",
            "MenuMusicReplacer.ba2",
            "BullBarrel.ba2",
            "EVB76NevernudeFemale - Meshes.ba2",
            "EVB76NevernudeFemale - Textures.ba2",
            "EVB76NevernudeMale - Meshes.ba2",
            "EVB76NevernudeMale - Textures.ba2",
            "EVB76 - Meshes.ba2",
            "EVB76 - Textures.ba2",
            "EVB76Nevernude - Meshes.ba2",
            "EVB76Nevernude - Textures.ba2",
            "BoxerShorts.ba2",
            "MaleUnderwear.ba2",
            "FemaleUnderwear.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceIndexFileList",
        "mods": [
            "UHDmap.ba2",
            "EnhancedBlood - Textures.ba2",
            "EnhancedBlood - Meshes.ba2",
            "MapMarkers.ba2",
            "Radiant_Clouds.ba2",
            "SpoilerFreeMap.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceArchive2List",
        "mods": [
            "PerkLoadoutManager.ba2",
            "ChatMod.ba2",
            "ShowHealthReRedux.ba2",
            "ShowHealth.ba2",
            "CompatibleShowHealthRedux.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
]
# The array index from the RESOURCE_MAP for sResourceArchive2List
SR_2LIST_INDEX = 3
MOD_TO_PLACE_LAST = "HUDModLoader.ba2"

# Re-run the program with admin rights if needed
if is_admin:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit(0)

# Create any missing folders
os.makedirs(os.path.dirname(ini_file_path), exist_ok=True)

# Validate that the data folder exists
if not os.path.exists(mods_dir):
    print(f"Error: Data folder '{mods_dir}' does not exist!")
    sys.exit(1)

print(f"Scanning for mods in: {mods_dir}")
print(f"Creating ini file at: {ini_file_path}")

# Open the Custom.ini file for writing
try:
    with open(ini_file_path, "w+", encoding="utf-8") as custom_ini_file:
        # Write the section header to the file
        custom_ini_file.write("[Archive]\r\n")

        # Loop through the resource map and add mods to the correct places
        for _, _, filenames in os.walk(mods_dir):
            for file in filenames:
                # Make sure the file is not an official file (starts with "SeventySix")
                # and is a ba2 (file extension)
                if not file.startswith("SeventySix") and file.lower().endswith(".ba2"):
                    found = False
                    for resource in RESOURCE_MAP:
                        if file in resource["mods"]:
                            resource["found_mods"].append(file)
                            found = True
                            break
                    # If a mod doesn't appear in the one of the other mod lists, add it to the default
                    if not found:
                        RESOURCE_MAP[SR_2LIST_INDEX]["found_mods"].append(file)
            break

        # Loop through the resource map and add the correct lines to the ini file
        for resource in RESOURCE_MAP:
            if resource["found_mods"]:
                found_mods = set(resource["found_mods"])
                mods = resource["mods"]
                mod_list = ", ".join(mod for mod in mods if mod in found_mods)

                # Get any mods that don't show up in the mods list (for the default list)
                diff_list = [item for item in found_mods if item not in mods]
                if diff_list:
                    diff_list.sort()

                    # Ensure MOD_TO_PLACE_LAST is at the end of the list
                    if MOD_TO_PLACE_LAST in diff_list:
                        diff_list.remove(MOD_TO_PLACE_LAST)
                        diff_list.append(MOD_TO_PLACE_LAST)

                    diff_list = ", " + ", ".join(diff_list)
                else:
                    diff_list = ""

                # Make the default list a string
                default_mods = ", ".join(resource["default_mods"])

                # Write the resource line to the ini file without leading comma
                line_content = "{}{}".format(default_mods, mod_list + diff_list)
                if line_content.startswith(", "):
                    line_content = line_content[2:]

                custom_ini_file.write(
                    "{} = {}\r\n".format(resource["filename"], line_content)
                )

        # Copy contents of a custom file into the custom.ini
        if import_ini:
            if os.path.exists(import_ini):
                with open(import_ini, "r", encoding="utf-8") as import_file:
                    custom_ini_file.write(import_file.read())
                print(f"Imported contents from: {import_ini}")
            else:
                print(f"Warning: Import file '{import_ini}' not found!")

    print(f"Successfully created {ini_file_path}")

except PermissionError:
    print(
        f"Error: Permission denied writing to '{ini_file_path}'. Try running with --runasadmin"
    )
    sys.exit(1)
except Exception as e:
    print(f"Error creating ini file: {e}")
    sys.exit(1)
