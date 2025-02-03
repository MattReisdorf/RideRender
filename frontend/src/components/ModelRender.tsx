import React, { useState, useEffect, useRef } from 'react';
import axios, { AxiosError } from 'axios'

import { Canvas, useLoader, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Mesh } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { BoardInfo } from './BoardInfo';
import { Modal } from 'antd';

import { LoadingOutlined } from '@ant-design/icons';


interface ModelRenderProps {
  brand: string | null,
  board: string | null,
  boardData: BoardsData
}

interface BoardsJSON {
  [key: string]: string[]
};

interface BoardModel {
  name: string,
  link: string,
  sizes: string[],
  price: string;
  [key: string]: string | string[]
}

interface BrandBoards {
  [modelName: string]: BoardModel;
}

interface BoardsData {
  [brand: string]: BrandBoards[]
}

export const ModelRender: React.FC<ModelRenderProps> = ({ brand, board, boardData }) => {
  const [modelExists, setModelExists] = useState<boolean>(false);
  const [errorThrown, setErrorThrown] = useState<boolean>(false);
  const [modelURL, setModelURL] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [modalOpen, setModalOpen] = useState<boolean>(false);


  const handleModalOpen = () => {
    setModalOpen(true);
  }

  const handleModalCloser = () => {
    setModalOpen(false);
  }

  const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  useEffect(() => {
    const checkModelExists = async () => {
      setErrorThrown(false);
      try {
        const response = await axios.post(`http://127.0.0.1:8000/model-existence/${board}/`);
        if (response.data.modelExists) {
          setModelExists(true);
        }
      }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          setErrorThrown(true);
        }
      }
    };

    const getGLBModel = async () => {
      setLoading(true)
      try {
        await delay(20000);
        const response = await axios.get<Blob>(`http://127.0.0.1:8000/get-glb-model/${board}/`, {
          responseType: 'blob'
        })
        const objectURL = URL.createObjectURL(response.data);
        setModelURL(objectURL)
        console.log(loading);
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
      finally {
        setLoading(false);
      }
    }

    if (brand != null && board != null) {
      checkModelExists();
      getGLBModel();
    }
  }, [brand, board])

  useEffect(() => {
    if (errorThrown) {
      setModalOpen(true);
    }
  }, [errorThrown])

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
      <Modal
        title = "Problem"
        centered
        open = {modalOpen}
        onOk = {() => setModalOpen(false)}
        onCancel = {() => setModalOpen(false)}
        footer = {null}
      >
        <p>
          There was an issue getting the board model.
        </p>
        <p>
          Please try another board, or try again later.
        </p>
      </Modal>
    );
  }

  if (loading) {
    return (
      <div
        style = {{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: 'auto'
        }}
      >
        <LoadingOutlined
          style={{
            display: 'flex',
            fontSize: '500px',
            color: 'yellow'
          }}
        />
      </div>
      
    )
  }

  if (modelURL && <Model modelURL={modelURL} />) {
    return (
      <>
        <BoardInfo board={board} brand={brand} boardData={boardData} />
        <div
          style={{
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
      </>

    )
  }

  return (null)
}