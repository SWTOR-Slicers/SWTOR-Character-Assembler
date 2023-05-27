# SWTOR Character Locator

This Blender Addon reproduces the function of the Slicers GUI tool's Locate feature as a Blender button in its 3D Viewers' sidebar, filling the selected Player Character or NPC's folder, exported by TORCommunity.com's Character Designer and NPC database, with all the game assets required for the .gr2 Importer Addon's Character Import feature to reconstruct them.

It adds a few novelties to the Locating process:
* Progress and error reporting through Blender's Console. It is recommended to keep it open to check for any error message, as it lists all the files it detects and copies, showing if any entry is malformed or leads to an inexistent file.
* It gathers a few extra texturemap types:
  * **DirectionMaps**, that can be used by the Creature, SkinB, and HairC Shaders.
  * **WrinklesMaps**, meant to be used in heads' SkinB Shaders (they don't support them yet, but some experiments are being carried in order to take advantage of them).
* It gathers too the character's **skeleton rig**, saving it inside a "skeleton" folder next to "models" and "materials".

The installation process is as any other standard Blender addon. In order to work, it requires us to set the path to a "resources" folder resulted from a game assets extraction through Slicers GUI (with presets "All" or "Dynamic") or EasyMYP. We do that in its Preferences panel.

The Addon appears in the 3D Viewport's Sidebar as a "SWTOR Char Locator" tab containing a single button. Instead of selecting a character's whole folder, it needs us to select the "path.json" file inside. Processing the file is nearly instantaneous. Once done, the character ought to be ready for import.

## **[Download the latest release](https://github.com/SWTOR-Slicers/SWTOR-Character-Locator/releases/latest)**
