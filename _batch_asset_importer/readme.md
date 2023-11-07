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

<br>

   4. Navigate inside unzipped 'Blender-Tools-main' folder and select '**batch_asset_importer.zip**' and click Install Add-On
<p align="center">
<img src="https://github.com/BlakeXYZ/Blender-Tools/assets/37947050/1bd89817-9221-4b3f-8539-36757cffce1d" width="700">
</p>
<br>

   5. Toggle On Add-On ☑️, a new Tab should be available now inside the N-Panel (Press N to open in 3D View)
<p align="center">
<img src="https://github.com/BlakeXYZ/Blender-Tools/assets/37947050/25e668b6-9d34-48e8-a22a-52e863736872" width="700">
</p>

____________
## <ins>Quick Start</ins>

#### Tool Vocabulary

- **_(3d) Asset_** : Packaged 3d File with complete PBR workflow.
- **_Root Pattern_** : User Naming Convention on Assets/Textures, anything before last '_' (underscore) is stored as root.
- **_Suffix Pattern_** : User Naming Convention on Textures, anything after last '_' (underscore) is stored as suffix.
  <br>
> ex: Glassy_Crystal_BC.png, root = 'Glassy_Crystal'  suffix = 'BC'

  <br>

#### File Extension Support

- **_Assets_** : [.fbx, .obj, .stl]
- **_Textures_** : [.bmp, .png, .jpg, .jpeg, .tga, .exr, .tif, .tiff]
  <br>
  <br>
  
#### Naming Convention Requirements

- The tool builds Materials based on Assets and Textures with matching **_Root Pattern_**.
- **_Root Pattern_** is determined by Asset Name
- Textures must only contain **_Root Pattern_** + **_Suffix Pattern_**
> :information_source: Texture **_Suffix Patterns_** currently supported:
  > _BC, _N, _ORM (packed occlusion, roughness, metalness)
  
<p align="center">
<img src="https://github.com/BlakeXYZ/Blender-Tools/assets/37947050/14a29d35-ef3c-4a69-8e29-57ea072b76a0" width="500">
</p>

  <br>

#### File Location Requirements

- Asset Files must be in one Folder
- Texture Files must be in one Folder
- Asset and Texture files do not need to sit in same Folder
> ☑️ Toggle on 'Are Texture Files in Different Path?' and select Texture File Location if above is True.



______
## <ins>Documentation</ins>

Provide a link to more detailed documentation if it exists. This could be a link to a separate documentation file or an external website. Include information on where users can find additional resources, tutorials, or support.

<p align="center">
<img src="" width="700">
</p>


