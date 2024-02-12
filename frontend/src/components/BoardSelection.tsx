import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Drawer } from 'antd';
import { LeftOutlined, RightOutlined, DoubleLeftOutlined, DoubleRightOutlined } from '@ant-design/icons';

// import { ImageDisplay } from './ImageDisplay';
// import { ModelRender } from './ModelRender';

import '../styles/BoardSelection.css';




interface BoardsJSON {
    [key: string]: string[]
};

export default function BoardSelection() {
    const [boards, setBoards] = useState<BoardsJSON>({});
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const getBoards = async() => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/boards-json')
                const boards: BoardsJSON = response.data.boards;
                setBoards(boards)
            }
            catch (error) {
                console.error(error)
            }
        }
        getBoards();
        setTimeout(() => {
            setLoading(false)
        }, 1000);
    }, []);

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
        setBrandDrawerOpen(!brandDrawerOpen);
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
                {Object.keys(boards).map((key) => (
                    <Button
                        className = 'brandDrawerButton'
                        key = {key}
                        type = 'link'
                        onClick = {() => handleBrandSelect(key)}
                    >
                        <img className = 'logoButton' src = {`/images/logos/${key}.jpg`} alt = {key} />
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
                {
                    selectedBrand
                    ?
                    boards[selectedBrand].map((board: string, index: number) => (
                        <div className = 'boardImageContainer'>
                            <Button
                                className = 'boardDrawerButton'
                                key = {index}
                                type = 'link'
                                onClick = {() => handleBoardSelect(board)}
                            >
                                <img
                                    className = 'boardButton'
                                    src = {
                                        selectedBrand == 'Yes'
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
                }
            </Drawer>

            <div>
                {/* <ImageDisplay brand = {selectedBrand} board = {selectedBoard} /> */}
                {/* <ModelRender /> */}
            </div>

        </>
    )
};