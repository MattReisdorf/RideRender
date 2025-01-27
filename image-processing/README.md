# Generating Models

- Run the {name} script, this will run all of the scripts to scrape the images and generate .obj models and .mtl texture files
- You'll need Blender to finish creating the .gltf model files with actual textures
    - I'm hoping to update the scripts in the future to handle this, but I want to get the site live sooner rather than later
- GLTF Steps:
    1. Import the textured .obj (-texture.obj) file for any board, not the .mtl
    ![alt text](import.png)

    2. Blender opens in Object mode by default, press "Tab" to switch to Edit mode, then press 3 to switch to face selection. Press "A" to select the entire model. In the right side properties menu, go down to "Material Properties". You should see the top and bottom textures in the menu at the top. I've been creating a new texture with the "+" symbol next to that menu to color the entire board since the base model color doesn't tend to match any of the actual texture colors. If you do that, click on the newly created texture in the list, then click on assign. This colors the entire model. ![alt text](base_color.png) NOTE: Make sure you are in "Material Preview Mode". This option is the 3rd of 4 in the top right of the viewing window. Looks like a sphere with a quadrant shaded white. 

    3. Now for the actual textures, click on the +Y direction face; this is the top sheet. Then click on the top sheet texture in the material list and click assign. This should assign the texture to that face. Do the same for the -Y direction and the bottom sheet texture. (Cardinal Directions are in the top right of the view window in case you missed them.). It won't look like much yet; we'll need to do some UV unwrapping to map the textures. ![alt text](assigned-textures.png)

    4. Select the +Y direction top face by left-clicking, press "U", then select "Smart UV Project", and click "Okay". This unwraps the UV mapping, and opens the context in a new window on the left. ![alt text](image.png) The entire mapping should be selected by default, but if it's not, press "A". Then right click on the texture and click "Unwrap". This should make the UV mapping fit the texture. You might have to rotate the mapping for some directional boards, not sure why it's upside down; I'm going to look into fixing that later. Do the same with the -Y direction botom face. UV mappings and be universally scaled if needed.

    5. You know have a textured model ![alt text](image-2.png) Export the model as a .glb file, that will preserve the textures and the model can be loaded with Three.js ![alt text](image-3.png)