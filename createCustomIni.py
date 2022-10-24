""" This module creates a fallout76Custom.ini file from the installed mods in the data directory """

import argparse
import ctypes
import errno
import os
from os import walk
import sys

# Set the default home and mod directories
HOME_DIR = os.path.expanduser("~") + "\\Documents\\My Games\\Fallout 76"
FILENAME = 'Fallout76Custom.ini'

# Get arguments from the user
PARSER = argparse.ArgumentParser(description='This program will automatically create the '
                                 + 'Fallout76Custom.ini file for you. In most cases the '
                                 + 'default arguments will be fine.')
PARSER.add_argument('--datafolder', default='.',
                    help='Specify fallout76\'s data folder location (Default: current directory)')
PARSER.add_argument('--inifolder', default=HOME_DIR,
                    help='Specify the folder where Fallout76Custom.ini lives'+
                    ' (Default: ' + HOME_DIR + ')')
PARSER.add_argument('--inifilename', default=FILENAME,
                    help='Specify the filename for the ini (Default: ' + FILENAME + ')')
PARSER.add_argument('--runasadmin', action="store_true",
                    help='Runs as an admin. Use when Fallout 76'
                    + 'installed in UAC location.')
PARSER.add_argument('--copyinicontents',
                    help='Copy a file\'s contents into your custom .ini')

ARGS = PARSER.parse_args()

# Assign arguments to variables
MODS_DIR = ARGS.datafolder
FILENAME = ARGS.inifilename
HOME_DIR = ARGS.inifolder + "\\" + FILENAME
IS_ADMIN = ARGS.runasadmin
IMPORT_INI = ARGS.copyinicontents

# Configuration arrays, these are mods that should go in specific
# lists, all other go in sResourceArchive2List
RESOURCE_MAP = [
    {
        'filename': 'sResourceStartUpArchiveList',
        'mods': [
            'BakaFile - Main.ba2',
            'IconTag.ba2',
            'IconSortingRatmonkeys.ba2',
            'MMM - Country Roads.ba2',
			'ImpUlt.ba2',
			'ImpUlt.ba2',
			'Quizzless Apalachia.ba2'
            ],
        'default_mods': [
            'SeventySix - Interface.ba2',
            'SeventySix - Localization.ba2',
            'SeventySix - Shaders.ba2',
            'SeventySix - Startup.ba2'
            ],
        'found_mods': []
    },
    {
        'filename': 'sResourceArchiveList2',
        'mods': [
			'PerkLoadoutManager.ba2',
			'IUMesh.ba2',
            'MoreWhereThatCameFrom.ba2',
            'Prismatic_Lasers_76_Lightblue.ba2',
            'OptimizedSonar.ba2',
            'Silentchameleon.ba2',
            'CleanPip.ba2',
            'classicFOmus_76.ba2',
            'nootnoot.ba2',
            'MenuMusicReplacer.ba2',
            'BullBarrel.ba2',
			'EVB76NevernudeFemale - Meshes.ba2',
			'EVB76NevernudeFemale - Textures.ba2',
			'EVB76NevernudeMale - Meshes.ba2',
			'EVB76NevernudeMale - Textures.ba2',
			'EVB76 - Meshes.ba2',
			'EVB76 - Textures.ba2',
			'EVB76Nevernude - Meshes.ba2',
			'EVB76Nevernude - Textures.ba2',
			'BoxerShorts.ba2',
			'MaleUnderwear.ba2',
			'FemaleUnderwear.ba2'
            ],
        'default_mods': [
            'SeventySix - Animations.ba2',
            'SeventySix - EnlightenInteriors.ba2',
            'SeventySix - GeneratedTextures01.ba2',
            'SeventySix - GeneratedTextures02.ba2',
            'SeventySix - WorkshopIcons.ba2',
            'SeventySix - EnlightenExteriors01.ba2',
            'SeventySix - EnlightenExteriors02.ba2'
            ],
        'found_mods': []
    },
    {
        'filename': 'sResourceIndexFileList',
        'mods': [
            'UHDmap.ba2',
            'EnhancedBlood - Textures.ba2',
            'EnhancedBlood - Meshes.ba2',
            'MapMarkers.ba2',
            'Radiant_Clouds.ba2',
            'SpoilerFreeMap.ba2',
            ],
        'default_mods': [
            'SeventySix - Textures01.ba2',
            'SeventySix - Textures02.ba2',
            'SeventySix - Textures03.ba2',
            'SeventySix - Textures04.ba2',
            'SeventySix - Textures05.ba2',
            'SeventySix - Textures06.ba2',
            'SeventySix - Textures07.ba2',
            'SeventySix - Textures08.ba2'
            ],
        'found_mods': []
    },
    {
        'filename': 'sResourceArchive2List',
        'mods': [
            'PerkLoadoutManager.ba2',
            'ChatMod.ba2',
            'ShowHealthReRedux.ba2',
            'ShowHealth.ba2',
            'CompatibleShowHealthRedux.ba2'
        ],
        'default_mods': [
        'SeventySix - StaticMeshes.ba2'
            ],
        'found_mods': []
    },
]
#The array index from the RESOURCE_MAP for sResourceArchive2List
SR_2LIST_INDEX = 3

# madogs: checks if user set --runasadmin=True
if IS_ADMIN:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
else:
    # Create any missing folders
    if not os.path.exists(os.path.dirname(HOME_DIR)):
        try:
            os.makedirs(os.path.dirname(HOME_DIR))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Open the Custom.ini file for writing
    CUSTOM_INI_FILE = open(HOME_DIR, "w+")

    # write the section header to the file
    CUSTOM_INI_FILE.write("[Archive]\r\n")

    # Loop through the resource map and add mods to the correct places
    for (dirpath, dirnames, filenames) in walk(MODS_DIR):
        for file in filenames:
            # Make sure the file is not an official file (starts with "SeventySix")
            # and is a ba2 (file extension)
            if (file[0:10] != 'SeventySix' and file[-4:].lower() == '.ba2'):
                FOUND = False
                for RESOURCE in RESOURCE_MAP:
                    if file in RESOURCE['mods']:
                        RESOURCE['found_mods'].append(file)
                        FOUND = True

                # If a mod doesn't appear in the one of the other mod lists, add it to the default
                if not FOUND:
                    RESOURCE_MAP[SR_2LIST_INDEX]['found_mods'].append(file)
        break

    # Loop through the resource map and add the correct lines to the ini file
    for RESOURCE in RESOURCE_MAP:
        if RESOURCE['found_mods']:
            # [TODO] Get the array intersection of the `mods` to the found mods
            # to make a sorted list based on what's in the map
            FOUND = frozenset(RESOURCE['found_mods'])
            MODS = RESOURCE['mods']
            MOD_LIST = [mod for mod in MODS if mod in FOUND]
            MOD_LIST = ', ' + ', '.join(MOD_LIST)

            # Get any mods that don't show up in the mods list (for the default list)
            DIFF_LIST = [item for item in FOUND if item not in MODS]
            if DIFF_LIST:
                DIFF_LIST.sort()
                DIFF_LIST = ', ' + ', '.join(DIFF_LIST)
            else:
                DIFF_LIST = ''

            # Make the default list a string
            DEFAULT_MODS = ', '.join(RESOURCE['default_mods'])

            CUSTOM_INI_FILE.write(
                RESOURCE['filename'] + " = %s\r\n"
                % (DEFAULT_MODS + MOD_LIST + DIFF_LIST)
            )

    # Copy contents of a custom file in to the custom.ini
    if IMPORT_INI:
        IMPORT_FILE = open(IMPORT_INI, "r")
        CUSTOM_INI_FILE.write(IMPORT_FILE.read())

    CUSTOM_INI_FILE.close()
