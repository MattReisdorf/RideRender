import React, { useState, useEffect }from 'react';
// import axios, { AxiosError } from 'axios'

import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { TextureLoader, Mesh, MeshStandardMaterial, MeshBasicMaterial, DoubleSide, FrontSide, BackSide } from 'three';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

// import { MeshBasicMaterial } from 'three';




function App() {


  const gltf = useLoader(GLTFLoader, 'yes-warca-uninc-jps-2024.glb')


  // const materials = useLoader(MTLLoader, 'Arbor-Annex-Camber.mtl');
  // console.log(materials);

  // const object = useLoader(OBJLoader, 'Arbor-Annex-Camber.obj', loader => {
  //   materials.preload();
  //   loader.setMaterials(materials)
  // });
  // console.log(object);

  // object.traverse((child) => {
  //   if (child.isMesh) {
  //     child.geometry.computeVertexNormals();
  //   }
  // })

  // object.traverse((child) => {
  //   if (child.isMesh) {
  //     child.material = new MeshBasicMaterial({ color: 0xff0000, side: DoubleSide })
  //   }
  // })

  return (
    <div style = {{
      // backgroundColor: "red",
      height: '100vh',
      width: '100vw'
    }}>
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <directionalLight position={[-10, -10, -5]} intensity={1} />
      {/* <primitive object={modelOBJ} scale={[2, 2, 2]}/> */}
      <primitive object={gltf.scene} />
      {/* <primitive object = {modelOBJBack} /> */}
      <OrbitControls />
    </Canvas>
    </div>
  );
}

export default App;
