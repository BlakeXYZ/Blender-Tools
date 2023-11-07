# Batch Asset Importer

## <ins>Overview</ins>

<div align="center">
Batch import 3d Assets + Textures and dynamically build Shader Graph per Asset using imported Textures.
</div>

#### Pipeline Problem:
 - Manually setting up a PBR Material for an Asset is a clunky and time consuming process. For each Asset user must: File > Import Panel, jump into Shader Graph, import each PBR Texture and then build the Shader graph with correct PBR Node layout. The 'Batch Asset Importer' tool automates these steps, now the user only needs to select Folder(s) that contain Assets + respective Textures and press 'Batch Import Assets'.


#### Built with:
 - Blender embedded Python 3.10.1


______
## <ins>Installation</ins>

   1. Download '[Blender-Tools](https://github.com/BlakeXYZ/Blender-Tools/tree/main)' Repo

<p align="center">
<img src="https://github.com/BlakeXYZ/Blender-Tools/assets/37947050/5ac0e8ae-e826-4113-8e1a-6deba5bcf83a" width="700">
</p>



   2. Unzip '**Blender-Tools-main.zip**'
   3. Open **Blender** and navigate to install Add-on: <br>
      - Edit > Preferences > Add-ons > Install...
<p align="center">
<img src="https://github.com/BlakeXYZ/Blender-Tools/assets/37947050/e46e7e37-e0cf-4601-b022-dfe3dd2aaa09" width="700">
</p>



> ❗ If your /scripts path already contains custom userSetup.py, copy paste '**_your_daily_fun_fact**' userSetup.py **<em>code</em>** to prevent overwriting 
     
   Windows
```
\Users\USERNAME\Documents\maya\MAYAVRSION\scripts
```
____________
## <ins>Quick Start</ins>

Describe how to use your tool. Include examples or code snippets to illustrate common use cases. Explain any command-line options, configuration settings, or parameters that users need to be aware of.

<div align="center">Batch Automate moving of Assets into new Folders based on User selected Assets and User input Folder names.
</div>
<br>

<p align="center">
   
<img src="https://github.com/BlakeXYZ/Unreal-Engine-Tools/assets/37947050/2f0ccaa9-be51-4b83-b4d6-8cdfcd959654" width="700">
</p>

______
## <ins>Documentation</ins>

Provide a link to more detailed documentation if it exists. This could be a link to a separate documentation file or an external website. Include information on where users can find additional resources, tutorials, or support.

<p align="center">
<img src="" width="700">
</p>


