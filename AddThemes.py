# coding: utf-8
import argparse
import os
from xml.etree import ElementTree as ET
from shutil import copy
from pathlib import Path
from pprint import pprint

parser = argparse.ArgumentParser(description='Themes')
parser.add_argument("themeDir",
					help="Path (relative to script) to the folder with the .xml theme files, default is ./themes",
					type=Path,
					nargs='?', # optional argument with default as fallback
					default="./themes")

parser.add_argument("cmderCfgDir",
					help="Path (relative to script) to your ConEmu folder where the ConEmu.xml file resides, default is ./../vendor/conemu-maximus5/",
					type=Path,
					nargs='?', # optional argument with default as fallback
					default="./../vendor/conemu-maximus5/")

parser.add_argument("-v", "--verbose",
					help="Enable verbose output",
					action="store_true")

parser.add_argument("-s", "--skip-backup",
					help="Don't create a backup config file before adding theme to ConEmu.xml",
					action="store_false")

args = parser.parse_args()

themeDir = args.themeDir.resolve()
configDir = args.cmderCfgDir.resolve()

print(themeDir)
print(configDir)

verbose = args.verbose
shouldBackup = args.skip_backup

curCfgName = "ConEmu.xml"
absCurCfg = os.path.join(configDir, curCfgName)

# Check if ConEmu.xml exists in cmderCfgDir
if not os.path.isfile( absCurCfg ):
	print(f"Unable to locate {curCfgName} in {configDir}, exiting...")
	exit()

if verbose:
	print(f"\nThemes Directory: {themeDir}")
	print(f"Cmder Config Directory: {configDir}\n")

if shouldBackup:
	i = 1
	#Increment file_name until we find one that doesn't exist
	while os.path.isfile(f"{absCurCfg}-{i}"):
		i += 1

	# and then copy and name the file
	backupName = f"{curCfgName}-{i}"
	absBackup = os.path.join(configDir, backupName)
	copy(absCurCfg, absBackup)

	if verbose: print(f"Created backup '{absBackup}'\n")

cfg = ET.parse(absCurCfg).getroot()
nodes = cfg[0][0].findall("key")

# set colorsNode equal to the node with name colors, i.e the <key name="Colors"> tag that holds the themes
for node in nodes:
	if node.attrib['name'] == "Colors":
		colorsNode = node
		break

if colorsNode == None:
	print(f"Could not find colors node in {absCurCfg}, exiting...")
	exit()
#elif verbose: print(f"Found colors node in {absCurCfg}")


# Find count node starting from the last element
for i in range( len(colorsNode) ):
	if colorsNode[-i].attrib['name'] == "Count":
		countNode = colorsNode[-i]
		break

if countNode == None:
	print(f"Could not find count node in the colors node in {absCurCfg}, exiting...")
	exit()
#elif verbose: print(f"Found count node in {absCurCfg}")


# For counting themes and updating countNode data attrib
themesAdded = 0

for root, dirs, files in os.walk(themeDir):
	for file in files:
		if file.endswith(".xml"):
			absThemePath = os.path.join(themeDir, file)
			if verbose: print(f"Appending theme {absThemePath}")

			# newThemeNode is the <key> tag that holds the theme colors and name
			newThemeNode = ET.parse(absThemePath).getroot()
			newThemeName = newThemeNode.attrib['name']

			# the themes are set up as such that
			# new themes root <key> element should have an attribute like: name='PaletteX'
			# and also contain exactly 39 keys
			# if it doesn't fit the criteria, move on to the next file
			if not newThemeName.startswith("Palette") or not len(newThemeNode) == 39:
				print(f"Malformed XML: {file}, skipping...")
				continue

			# The colors node has the already existing theme nodes and one "metadata/length" node
			# so the length will always equal what the new palette index should be
			paletteIndex = len(colorsNode)
			newThemeNode.attrib['name'] = f"Palette{paletteIndex}"

			# Append new theme
			colorsNode.insert(-1, newThemeNode)
			# Increment <value> element that has data attrib which should equal the number of themes
			themesAdded += 1

#update count node to reflect new/current length
countNode.attrib['data'] = str( int(countNode.attrib['data'])+themesAdded )

absNewCfg = absCurCfg # In place of the old config
with open(absNewCfg, 'wb') as newCfgFile:
	newConfig = ET.tostring(cfg, encoding='utf-8', method='xml')
	newCfgFile.write(newConfig)


print(f"All done! {themesAdded} theme(s) added")