"""
This module creates a fallout76Custom.ini file from the installed mods in the data directory
"""

import argparse
import ctypes
import os
import sys

# Set the default home and mod directories
HOME_DIR = os.path.expanduser("~") + "\\Documents\\My Games\\Fallout 76"
FILENAME = "Fallout76Custom.ini"

# Get arguments from the user
parser = argparse.ArgumentParser(
    description="This program will automatically create the "
                "Fallout76Custom.ini file for you. In most cases the "
                "default arguments will be fine."
)
parser.add_argument(
    "--datafolder",
    default=".",
    help="Specify Fallout 76's data folder location (Default: current directory)"
)
parser.add_argument(
    "--inifolder",
    default=HOME_DIR,
    help="Specify the folder where Fallout76Custom.ini lives (Default: {})".format(HOME_DIR)
)
parser.add_argument(
    "--inifilename",
    default=FILENAME,
    help="Specify the filename for the ini (Default: {})".format(FILENAME)
)
parser.add_argument(
    "--runasadmin",
    action="store_true",
    help="Runs as an admin. Use when Fallout 76 is installed in UAC location."
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

# Re-run the program with admin rights if needed
if is_admin:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

# Create any missing folders
os.makedirs(os.path.dirname(ini_file_path), exist_ok=True)

# Open the Custom.ini file for writing
with open(ini_file_path, "w+") as custom_ini_file:
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
        with open(import_ini, "r") as import_file:
            custom_ini_file.write(import_file.read())
