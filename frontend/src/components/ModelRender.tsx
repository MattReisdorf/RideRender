import React, { useState, useEffect }from 'react';
import axios, { AxiosError } from 'axios'

import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { TextureLoader, Mesh, MeshStandardMaterial, MeshBasicMaterial, FrontSide, BackSide } from 'three';




interface ModelRenderProps {
    brand: string | null,
    board: string | null
}

export const ModelRender: React.FC<ModelRenderProps> = ({brand, board}) => {

    const [manufacturer, setManufacturer] = useState<string | null>(null);
    const [model, setModel] = useState<string | null>(null);
    const [modelExists, setModelExists] = useState<boolean>(false);
    const [errorThrown, setErrorThrown] = useState<boolean>(false);

    const [defaultTexturePath, setDefaultTexturePath] = useState<string>('/images/mens/Burton/splits/Burton-Family-Tree-3D-Daily-Driver/Burton-Family-Tree-3D-Daily-Driver_0.jpg')

    useEffect(() => {
        const checkFileExists = async() => {
            try {
                const makeModel = {
                    brand: brand,
                    board: board
                };
                const response = await axios.post('http://127.0.0.1:8000/model-existence/', makeModel)
                if (response.data.modelExists) {
                    console.log(response.data.path)
                    setDefaultTexturePath(response.data.path)
                    setDefaultTexturePath(defaultTexturePath.replace('E:/Projects/RideRender/frontend/public', '').replace('models', 'splits').replace('.obj', '_0.jpg').replace(/\\/g, '/'))
                    setManufacturer(brand)
                    setModel(board)
                }
            }
            catch (error: unknown) {
                if (axios.isAxiosError(error)) {
                    const requestError = error as AxiosError;
                    if(requestError.response?.status !== 200) {
                        setErrorThrown(true)
                    }
                }
            }
        };
        checkFileExists();
    }, [brand, board]);

    const modelPath = (
        manufacturer === 'Yes'
        ?
        `/images/mens/${manufacturer}/models/${manufacturer?.replace(/ /g, '-')}.-${model?.replace(/ /g, '-')}/${manufacturer?.replace(/ /g, '-')}.-${model?.replace(/ /g, '-')}.obj`
        :
        `/images/mens/${manufacturer}/models/${manufacturer?.replace(/ /g, '-')}-${model?.replace(/ /g, '-')}/${manufacturer?.replace(/ /g, '-')}-${model?.replace(/ /g, '-')}.obj`
    );

    // const texturePath = (
    //     manufacturer === 'Yes'
    //     ?
    //     `/images/mens/${manufacturer}/splits/${manufacturer?.replace(/ /g, '-')}.-${model?.replace(/ /g, '-')}/${manufacturer?.replace(/ /g, '-')}.-${model?.replace(/ /g, '-')}_0.jpg`
    //     :
    //     `/images/mens/${manufacturer}/splits/${manufacturer?.replace(/ /g, '-')}-${model?.replace(/ /g, '-')}/${manufacturer?.replace(/ /g, '-')}-${model?.replace(/ /g, '-')}_0.jpg`
    // )


    console.log(defaultTexturePath)
    // if (modelExists) {
    //     const modelOBJ = useLoader(OBJLoader, modelPath)
    //     const texture = useLoader(TextureLoader, texturePath)
    //     modelOBJ.traverse((child) => {
    //         if ((child as Mesh).isMesh) {
    //           const mesh = child as Mesh;
    //           if (Array.isArray(mesh.material)) {
    //             mesh.material.forEach((material) => {
    //               if (material instanceof MeshStandardMaterial) {
    //                 material.map = texture;
    //               }
    //             });
    //           } else if (mesh.material instanceof MeshStandardMaterial) {
    //             mesh.material.map = texture;
    //           }
    //         }
    //       });
    // }


    const modelOBJFront = useLoader(OBJLoader, modelPath)
    const texture = useLoader(TextureLoader, defaultTexturePath);

    const frontMaterial = new MeshBasicMaterial({ color: 'black', side: FrontSide })
    const backMaterial = new MeshBasicMaterial({ color: 'red', side: BackSide })

    // modelOBJFront?.traverse((child) => {
    //     if ((child as Mesh).isMesh) {
    //         const mesh = child as Mesh;
    //         if (Array.isArray(mesh.material)) {
    //         mesh.material.forEach((material) => {
    //             if (material instanceof MeshStandardMaterial) {
    //             material.map = texture;
    //             }
    //         });
    //         } else if (mesh.material instanceof MeshStandardMaterial) {
    //         mesh.material.map = texture;
    //         }
    //         (child as Mesh).material = frontMaterial
    //     }
    //     });

    // const modelOBJBack = modelOBJFront.clone()
    // modelOBJBack.traverse((child) => {
    //     if((child as Mesh).isMesh) {
    //         (child as Mesh).material = backMaterial
    //     }
    // })

    // const texture = useLoader(TextureLoader, texturePath)

    // modelOBJ.traverse((child) => {
    //     if ((child as Mesh).isMesh) {
    //         (child as Mesh).material.map = texture;
    //     }
    // })
    // modelOBJ.traverse((child) => {
    //     if ((child as Mesh).isMesh) {
    //         const mesh = child as Mesh
    //         if (Array.isArray(mesh.material)) {
    //             mesh.material.forEach((material) => {
    //                 if (material instanceof MeshStandardMaterial) {
    //                     material.map(texture)
    //                 }
    //             })
    //         }
    //     }
    // })

    modelOBJFront.traverse((child) => {
        if ((child as Mesh).isMesh) {
          const mesh = child as Mesh;
          if (Array.isArray(mesh.material)) {
            mesh.material.forEach((material) => {
              if (material instanceof MeshStandardMaterial) {
                material.map = texture;
              }
            });
          } else if (mesh.material instanceof MeshStandardMaterial) {
            mesh.material.map = texture;
          }
        }
      });

    if (errorThrown) {
        return (
            <div>
                <span>There was a problem getting the model, please try again later</span>
            </div>
        );
    }

    else if (manufacturer && model) {

        return (
            <Canvas>
                <ambientLight intensity={0.5} />
                <directionalLight position={[10, 10, 5]} intensity={1} />
                <directionalLight position={[-10, -10, -5]} intensity={1} />
                {/* <primitive object={modelOBJ} scale={[2, 2, 2]}/> */}
                <primitive object={modelOBJFront} />
                {/* <primitive object = {modelOBJBack} /> */}
                <OrbitControls />
            </Canvas>


        )
    }




    return(null)
}