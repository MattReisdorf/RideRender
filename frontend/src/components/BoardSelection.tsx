import React, { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import { Button, Drawer } from 'antd';
import { DoubleLeftOutlined, DoubleRightOutlined } from '@ant-design/icons';

import { ImageDisplay } from './ImageDisplay';
import { ModelRender } from './ModelRender';
import '../styles/BoardSelection.css';

// import boardData from '../../public/board-info.json';

// console.log(boardData)




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
export default function BoardSelection() {
    const [boards, setBoards] = useState<BoardsData>({});
    const [errorThrown, setErrorThrown] = useState<boolean>(false);

    useEffect(() => {
        const getBoards = async() => {
            try {
                // const response = await axios.get('http://127.0.0.1:8000/boards-json')
                const response = await axios.get('/board-info.json')
                // console.log(response);
                const boards = response.data;
                setBoards(boards)
            }
            catch (error: unknown) {
                if (axios.isAxiosError(error)) {
                    const requestError = error as AxiosError;
                    if (requestError.response?.status !== 200) {
                        console.warn = () => {};
                        setErrorThrown(true);
                    }
                }
            }
        }
        getBoards();
        setTimeout(() => {
        }, 1000);
    }, []);

    // console.log(boards);

    

    const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
    const [selectedBoard, setSelectedBoard] = useState<string | null>(null);
    const [brandDrawerOpen, setBrandDrawerOpen] = useState<boolean>(false);
    const [boardDrawerOpen, setBoardDrawerOpen] = useState<boolean>(false);

    const openBrandDrawer = () => {
        setBrandDrawerOpen(!brandDrawerOpen)
    };

    const handleBrandSelect = (brand: string) => {
        setSelectedBrand(brand);
        setBrandDrawerOpen(!brandDrawerOpen);
        openBoardDrawer();
    };

    const openBoardDrawer = () => {
        setBoardDrawerOpen(!boardDrawerOpen);
        // setBrandDrawerOpen(!brandDrawerOpen);
    };

    const handleBoardSelect = (board: string) => {
        setSelectedBoard(board);
        setBoardDrawerOpen(!boardDrawerOpen);
    };

    const handleCloseBrandDrawer = () => {
        setBrandDrawerOpen(false);
    };

    const handleCloseBoardDrawer = () => {
        setBoardDrawerOpen(false);
    };


    if (errorThrown) {
        return (
            <div>
                <span>Error Thrown</span>
            </div>
        )
    }

    // console.log(selectedBrand, selectedBoard);

    // if(selectedBrand) {
    //   boards[selectedBrand].map((board: BrandBoards) => {
    //     const boardNames = Object.keys(board);
    //     const boardName = boardNames[0];
    //     const boardDetails = board[boardName];
    //     console.log(boardDetails.name)
    //   })
    // }

    return (
        <>
            <Button 
                className = {`closedBrandDrawerButton ${brandDrawerOpen ? 'openedBrandDrawerButton' : ''} ${boardDrawerOpen ? 'hidden' : ''}`}
                type = 'text'
                onClick = {openBrandDrawer}
            >
                {
                    !boardDrawerOpen
                    ?
                    (!brandDrawerOpen ? <DoubleLeftOutlined /> : <DoubleRightOutlined />)
                    :
                    null
                }
            </Button>
            <Drawer
                placement = 'right'
                onClose = {handleCloseBrandDrawer}
                open = {brandDrawerOpen}
                closable = {false}
                className = 'brandDrawer'
                width = {348}
            >
                {Object.keys(boards).map((brand: string, index: number) => (
                    <Button
                        className = 'brandDrawerButton'
                        key = {index}
                        type = 'link'
                        onClick = {() => handleBrandSelect(brand)}
                    >
                        <img className = 'logoButton' src = {`/images/logos/${brand}.jpg`} alt = {brand} />
                    </Button>
                ))}
            </Drawer>
            <Button
                className = {`boardButtonTest ${boardDrawerOpen ? 'boardButtonFinal' : ''}`}
                type = 'text'
                onClick = {openBoardDrawer}
            >
                {!boardDrawerOpen ? <DoubleLeftOutlined /> : <DoubleRightOutlined />}
            </Button>
            <Drawer
                title = {<img className = 'selectedBrandLogo' src = {`/images/logos/${selectedBrand}.jpg`} />}
                placement = 'right'
                onClose = {handleCloseBoardDrawer}
                open = {boardDrawerOpen}
                className = 'boardDrawer'
                closeIcon = {false}
                width = {348}
            >
                {/* {
                    selectedBrand
                    ?
                    boards[selectedBrand].map((board: BrandBoards) => (
                        <div className = 'boardImageContainer' key = {board}>
                            <Button
                                className = 'boardDrawerButton'
                                type = 'link'
                                onClick = {() => handleBoardSelect(board)}
                            >
                                <img
                                    className = 'boardButton'
                                    src = {
                                        selectedBrand === 'Yes'
                                        ?
                                        `/images/mens/${selectedBrand}/${selectedBrand.replace(/ /g, '-')}.-${board.replace(/ /g, '-')}.jpg`
                                        :
                                        `/images/mens/${selectedBrand}/${selectedBrand.replace(/ /g, '-')}-${board.replace(/ /g, '-')}.jpg`
                                    }
                                    alt = {selectedBrand + " " + board} />
                                    <span className = 'boardButtonName'>{board}</span>
                            </Button>
                        </div>
                    ))
                    :
                    null
                } */}
                {
                selectedBrand
                  ? boards[selectedBrand].map((modelObject: BrandBoards) => {
                      // Extract the model name (e.g., "arbor-a-frame")
                      const modelName = Object.keys(modelObject)[0];
                      
                      // Access the BoardModel using the model name
                      const boardData = modelObject[modelName];
                      
                      return (
                        <div className='boardImageContainer' key={boardData.name}>
                          <Button
                            className='boardDrawerButton'
                            type='link'
                            onClick={() => handleBoardSelect(boardData.name)} // Pass the board name or adjust as needed
                          >
                            <img
                              className='boardButton'
                              src={
                                selectedBrand === 'Yes'
                                  ? `/images/mens/${selectedBrand}/${selectedBrand.replace(/ /g, '-')}.-${boardData.name.replace(/ /g, '-')}.png`
                                  // : `/images/mens/${selectedBrand}/${selectedBrand.replace(/ /g, '-')}-${boardData.name.replace(/ /g, '-')}.png`
                                  : `/images/mens/${selectedBrand}/${boardData.name}.png`
                              }
                              alt={`${selectedBrand} ${boardData.name}`}
                            />
                            <span className='boardButtonName'>{boardData.name}</span>
                          </Button>
                        </div>
                      );
                    })
                  : null
              }
            </Drawer>

            <div className = 'imageContainer'>
                {/* <ImageDisplay brand = {selectedBrand} board = {selectedBoard} /> */}
                <ModelRender brand = {selectedBrand} board = {selectedBoard}/>
            </div>

        </>
    )
};