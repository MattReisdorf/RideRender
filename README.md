# RideRender
![Demo GIF](./demo2.gif)

Site has been fully updated, should work end to end now.

*Still have a couple things that need to be cleaned up*
* Finish cleaning up models and get them uploaded
* Get the site live

*Things to be added eventually*
* Popup on first load to explain controls
* User controls for lighting and background
* UI improvements



### Old README
#### Keeping for Reference
![Demo GIF](./demo.gif)

~~Currently a Work in Progress~~

~~Ultimately, this is a site for viewing 3D models of snowboards purchasable from a large retailer.~~ 

~~Frontend is mostly complete, a couple things probably still need tweaking. ~~

~~Model generation is handled on the backend with python. Logic there is still the main blocker. Currently the models are only generated as single flat meshes, that I'm then doubling and applying some thickness to.~~

*Issues as of 12/17/24*
* Model: Flat meshes make flat models. Still need to ~~extrude depth and~~ fix the tip and tail curvature for all generated models.
* ~~Model: Clean up the edges on generated models. Models are generated from lower-than-desirable resolution images, causes some "spiking" along the edges~~ Fixed with Blender API
* ~~Model: Texturing still needs to be done, hopefully won't be a huge issue. Might be done on the Frontend with three, might need to do at model generation.~~ Partial Fix: Textures are assigned with Blender API, but still need to be manually placed in the Blender Application
* ~~Frontend: Model is scaled too small on first render, only affects the first board chosen. Once zoomed in, other selected boards keep the same scaling. Just need to change the default scale.~~
* ~~Frontend: Lower Priority; Can't cancel board selection without cancelling manufacturer selection. Not a huge deal, doesn't affect the site beyond user experience.~~