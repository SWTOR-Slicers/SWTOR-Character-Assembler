# SWTOR Character Assembler

**This Blender addon combines the functionality of the [Slicers GUI](https://github.com/SWTOR-Slicers/Slicers-GUI) tool's Locate feature and the [.gr2 Importer Addon](https://github.com/SWTOR-Slicers/Granny2-Plug-In-Blender-2.8x)'s Character Importer as an automated one-button process.**

It fills a Player Character/NPC's folder (exported by TORCommunity.com's Character Designer and NPC database) with all the game assets required for the .gr2 Importer Addon's Character Import feature to reconstruct them, and calls such addon to do the importing

It adds a few novelties to the Locating process:
* **It reports its progress and errors through Blender's Console**. It is recommended to keep it open to check for any error message, as it lists all the files it detects and copies, showing if any entry is malformed or leads to an inexistent file.
* **It places a "black.dds" file in `resources\art\defaultassets` if it is missing**.
* It gathers a few extra texturemap types:
  * **DirectionMaps**, that can be used by the Creature, SkinB, and HairC Shaders.
  * **WrinklesMaps**, meant to be used in heads' SkinB Shaders (they don't support them yet, but some experiments are being carried in order to take advantage of them).
* It gathers too the character or NPC's **skeleton rig**, saving it inside a "skeleton" folder next to "models" and "materials".

The installation process is as any other standard Blender addon. In order to work, it requires us to set the path to a "resources" folder resulted from a game assets extraction through Slicers GUI (with presets "All" or "Dynamic") or EasyMYP. We do that in its Preferences panel. If not set, the Addon's button will be greyed out.

The addon appears in the 3D Viewport's Sidebar as a "SWTOR Tools" tab containing a single button. Instead of selecting a character's whole folder as we used to do with the Slicers GUI tool, it needs us to select the "path.json" file inside, instead. Processing the file is nearly instantaneous.

There are some options checkboxes:

* **Gather Assets Only**: it only locates and copies the asset files to the character folder.
* **Don't Overwrite Assets**: if a located file already exists in the folder, it preserves it instead of overwriting it. Useful if the files in the folder have been modified in some manner, such as retouching a texture, without changing the name.

**WARNING: this addon doesn't solve the problem of character objects with two materials** (armor or clothes that let skin show, such as undergarments) showing the first material in the areas where the second material ought to show up. This is a bug in the .gr2 Importer Addon that is being investigated. As soon as it is solved there it will work correctly here, too.

## **[Download the latest release here](https://github.com/SWTOR-Slicers/SWTOR-Character-Locator/releases/latest)**
