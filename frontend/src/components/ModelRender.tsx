import React, { useState, useEffect, useRef } from 'react';
import axios, { AxiosError } from 'axios'

import { Canvas, useLoader, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Mesh } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

interface ModelRenderProps {
  brand: string | null,
  board: string | null
}

export const ModelRender: React.FC<ModelRenderProps> = ({ brand, board }) => {
  const [modelExists, setModelExists] = useState<boolean>(false);
  const [errorThrown, setErrorThrown] = useState<boolean>(false);
  const [modelURL, setModelURL] = useState<string | null>(null);

  useEffect(() => {

    const checkModelExists = async () => {
      try {
        const response = await axios.post(`http://127.0.0.1:8000/model-existence/${board}/`);
        if (response.data.modelExists) {
          setModelExists(true);
        }
      }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const requestError = error as AxiosError;
          if (requestError.response?.status !== 200) {
            setErrorThrown(true);
          }
        }
      }
    };

    const getGLBModel = async () => {
      try {
        const response = await axios.get<Blob>(`http://127.0.0.1:8000/get-glb-model/${board}/`, {
          responseType: 'blob'
        })
        console.log(response.data);
        const objectURL = URL.createObjectURL(response.data);
        setModelURL(objectURL)
      }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const requestError = error as AxiosError;
          if (requestError.response?.status !== 200) {
            console.log(error);
            setErrorThrown(true)
          }
        }
      }
    }
    
    if (brand != null && board != null) {
      checkModelExists();
      getGLBModel();
    }
  }, [brand, board])

  const Model = ({ modelURL }: { modelURL: string }) => {
    const modelRef = useRef<Mesh>(null!);
    useFrame(() => {
      modelRef.current.rotation.y = Math.PI;
    })
    const gltf = useLoader(GLTFLoader, modelURL);

    useThree(({ camera }) => {
      camera.position.z = 6;
      camera.lookAt(0, 0, 0)
    })

    return (
      <primitive
        object={gltf.scene}
        ref={modelRef}
      />
    );
  }


  if (errorThrown) {
    return (
      <div>
        <span>There was a problem getting the model, please try again later</span>
      </div>
    );
  }

  else if (modelURL && <Model modelURL={modelURL} />) {

    return (
      <div 
        style = {{
          height: 'auto',
          width: '30vw',
          marginLeft: 'auto',
          marginRight: 'auto',
          cursor: 'grab'
        }}
      >
        <Canvas>
          <ambientLight intensity={2} />
          <directionalLight position={[10, 10, 5]} intensity={1} />
          <directionalLight position={[-10, -10, -5]} intensity={1} />
          {modelURL && <Model modelURL={modelURL} />}
          <OrbitControls />
        </Canvas>
      </div>
    )
  }

  return (null)
}