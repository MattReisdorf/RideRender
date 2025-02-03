import React, { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import { Button, Drawer, Modal } from 'antd';
import { DoubleLeftOutlined, DoubleRightOutlined } from '@ant-design/icons';
import { ModelRender } from './ModelRender';
import '../styles/BoardSelection.css';

interface BoardModel {
  name: string;
  link: string;
  sizes: string[];
  price: string;
  [key: string]: string | string[];
}

interface BrandBoards {
  [modelName: string]: BoardModel;
}

interface BoardsData {
  [brand: string]: BrandBoards[];
}

export default function BoardSelection() {
  const [boards, setBoards] = useState<BoardsData>({});
  const [errorThrown, setErrorThrown] = useState<boolean>(false);
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [confirmedBrand, setConfirmedBrand] = useState<string | null>(null);
  const [confirmedBoard, setConfirmedBoard] = useState<string | null>(null);
  const [draftBrand, setDraftBrand] = useState<string | null>(null);
  const [draftBoard, setDraftBoard] = useState<string | null>(null);
  const [brandDrawerOpen, setBrandDrawerOpen] = useState<boolean>(false);
  const [boardDrawerOpen, setBoardDrawerOpen] = useState<boolean>(false);


  useEffect(() => {
    const getBoards = async () => {
      try {
        const response = await axios.get('/board-info.json');
        setBoards(response.data);
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const requestError = error as AxiosError;
          if (requestError.response?.status !== 200) {
            console.warn = () => {};
            setErrorThrown(true);
          }
        }
      }
    };
    getBoards();
  }, []);

  useEffect(() => {
    if (errorThrown) {
      setModalOpen(true);
    }
  }, [errorThrown])

  const openBrandDrawer = () => {
    setBrandDrawerOpen(true);
  };

  const handleBrandSelect = (brand: string) => {
    setDraftBrand(brand);
    setBoardDrawerOpen(true);
  };

  const handleBoardSelect = (board: string) => {
    setDraftBoard(board);

    setConfirmedBrand(draftBrand);
    setConfirmedBoard(board);

    setBrandDrawerOpen(false);
    setBoardDrawerOpen(false);
  };

  const handleCloseBoardDrawer = () => {
    setBoardDrawerOpen(false);
    setDraftBrand(null);
    setDraftBoard(null);
  };

  const handleCloseBrandDrawer = () => {
    setBrandDrawerOpen(false);
    setBoardDrawerOpen(false);
    setDraftBrand(null);
    setDraftBoard(null);
  };

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
          There was an issue, please try again later.
        </p>

      </Modal>
    );
  }

  return (
    <>
      <Button
        className={`closedBrandDrawerButton ${
          brandDrawerOpen ? 'openedBrandDrawerButton' : ''
        } ${boardDrawerOpen ? 'hidden' : ''}`}
        type="text"
        onClick={openBrandDrawer}
      >
        {!boardDrawerOpen ? (!brandDrawerOpen ? <DoubleLeftOutlined /> : <DoubleRightOutlined />) : null}
      </Button>

      <Drawer
        placement="right"
        onClose={handleCloseBrandDrawer}
        open={brandDrawerOpen}
        closable={false}
      >
        {Object.keys(boards).map((brand: string, index: number) => (
          <Button
            className="brandDrawerButton"
            key={index}
            type="link"
            onClick={() => handleBrandSelect(brand)}
          >
            <img className="logoButton" src={`/images/logos/${brand}.jpg`} alt={brand} />
          </Button>
        ))}

        <Drawer
          title={
            draftBrand ? (
              <img className="selectedBrandLogo" src={`/images/logos/${draftBrand}.jpg`} alt={draftBrand} />
            ) : (
              ''
            )
          }
          placement="right"
          onClose={handleCloseBoardDrawer}
          open={boardDrawerOpen}
          closable={false}
        >
          {draftBrand &&
            boards[draftBrand].map((modelObject: BrandBoards) => {
              const modelName = Object.keys(modelObject)[0];
              const boardData = modelObject[modelName];

              return (
                <div className="boardImageContainer" key={boardData.name}>
                  <Button
                    className="boardDrawerButton"
                    type="link"
                    onClick={() => handleBoardSelect(boardData.name)}
                  >
                    <img
                      className="boardButton"
                      src={
                        draftBrand === 'Yes'
                          ? `/images/mens/${draftBrand}/${draftBrand.replace(/ /g, '-')}.--${boardData.name.replace(/ /g, '-')}.png`
                          : `/images/mens/${draftBrand}/${boardData.name}.png`
                      }
                      alt={`${draftBrand} ${boardData.name}`}
                    />
                    <span className="boardButtonName">
                      {boardData.name
                        .replace(`${draftBrand}`, '')
                        .replace(/-/g, ' ')
                        .replace(/\b[a-z]/g, (match) => match.toUpperCase())}
                    </span>
                  </Button>
                </div>
              );
            })}
        </Drawer>
      </Drawer>

      {confirmedBrand && confirmedBoard && (
        <div className="imageContainer">
          <ModelRender brand={confirmedBrand} board={confirmedBoard} boardData={boards} />
        </div>
      )}
    </>
  );
}