import React, { useState, useEffect, useRef } from 'react';
import axios, { AxiosError } from 'axios';
import { Button, ConfigProvider, Divider, Drawer, Modal, theme, Tour, TourProps } from 'antd';
import { DoubleLeftOutlined, InfoCircleFilled, MoonFilled, SunFilled } from '@ant-design/icons';
import { ModelRender } from './ModelRender';
import '../styles/BoardSelection.css';
import '../styles/antdOverrides.css';
import { BoardInfo } from './BoardInfo';

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
  const [infoModalOpen, setInfoModalOpen] = useState<boolean>(true);
  const [tourOpen, setTourOpen] = useState<boolean>(false);
  const [tourKey, setTourKey] = useState<number>(0);
  const [windowWidth, setWindowWidth] = useState<number>(window.innerWidth);
  const [isDarkTheme, setIsDarkTheme] = useState<boolean>(false);
  const [lightOrDark, setLightOrDark] = useState<"light" | "dark">("light");

  const buttonRef = useRef(null);
  const brandRef = useRef(null);
  const boardRef = useRef(null);
  const modelRef = useRef(null);
  const infoRef = useRef(null);
  const themeRef = useRef(null);

  // const steps: TourProps['steps'] = [
  //   {
  //     title: 'Open Button',
  //     description: 'Click or Tap here to start.',
  //     target: () => buttonRef.current,
  //     nextButtonProps: {
  //       onClick: () => {
  //         setBrandDrawerOpen(true);
  //         setDraftBrand('arbor');
  //         console.log("Next Clicked");
  //       }
  //     },
  //     prevButtonProps: {
  //       onClick: () => {
  //         setBrandDrawerOpen(false);
  //         console.log("Prev Clicked");
  //       }
  //     },
  //     placement: 'left',
  //     onClose: () => {
  //       setTourOpen(false);
  //       setBrandDrawerOpen(false);
  //       setBoardDrawerOpen(false);
  //       setDraftBrand(null);
  //     }
  //   },
  //   {
  //     title: 'Brand Selection',
  //     description: 'Click or Tap any brand to select a board.',
  //     target: () => document.querySelector('.logoButton.arbor')!,
  //     nextButtonProps: {
  //       onClick: () => {
  //         setBoardDrawerOpen(true)
  //         setDraftBoard('arbor-a-frame')
  //       }
  //     },
  //     prevButtonProps: {
  //       onClick: () => {
  //         setBrandDrawerOpen(false);
  //         console.log("Prev Clicked");
  //       }
  //     },
  //     placement: 'bottom',
  //     onClose: () => {
  //       setTourOpen(false);
  //       setBrandDrawerOpen(false);
  //       setBoardDrawerOpen(false);
  //       setDraftBrand(null);
  //     }
  //   },
  //   {
  //     title: 'Board Selection',
  //     description: 'Click or Tap any board to load a model.',
  //     target: () => document.querySelector('.boardButton.arbor-a-frame')!,
  //     nextButtonProps: {
  //       onClick: () => {
  //         setBoardDrawerOpen(false);
  //         setBrandDrawerOpen(false);
  //         setConfirmedBoard(draftBoard);
  //         setConfirmedBrand(draftBrand);
  //         setDraftBrand(null);
  //         setDraftBoard(null);
  //       }
  //     },
  //     prevButtonProps: {
  //       onClick: () => {
  //         setBoardDrawerOpen(false);
  //       }
  //     },
  //     placement: 'bottom',
  //     onClose: () => {
  //       setTourOpen(false);
  //       setBrandDrawerOpen(false);
  //       setBoardDrawerOpen(false);
  //       setDraftBoard(null);
  //       setDraftBrand(null);
  //     }
  //   },
  //   {
  //     title: 'Model',
  //     description: 'The selected model will render here.\nDesktop: Click and Drag to rotate.\nMobile: Swipe to rotate.',
  //     target: null,
  //     nextButtonProps: {
  //       onClick: () => {
  //         setBoardDrawerOpen(false);
  //         setBrandDrawerOpen(false);
  //         setDraftBrand(null)
  //       }
  //     },
  //     prevButtonProps: {
  //       onClick: () => {
  //         setBoardDrawerOpen(false);
  //       }
  //     },
  //     onClose: () => {
  //       setTourOpen(false);
  //       setBrandDrawerOpen(false);
  //       setBoardDrawerOpen(false);
  //       setDraftBrand(null);
  //     }
  //   },
  //   {
  //     title: 'More Info',
  //     description: 'Click or Tap here to see more information.',
  //     target: () => document.querySelector('.boardInfoButton')!,
  //     placement: 'right'
  //   },
  //   {
  //     title: 'Theme',
  //     description: 'Switch between dark and light modes.',
  //     target: themeRef.current,
  //     placement: 'right'
  //   }
  // ]

  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  useEffect(() => {
    const getBoards = async () => {
      try {
        const response = await axios.get('/board-info.json');
        setBoards(response.data);
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const requestError = error as AxiosError;
          if (requestError.response?.status !== 200) {
            console.warn = () => { };
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

  useEffect(() => {
    isDarkTheme ? setLightOrDark('dark') : setLightOrDark('light');
  }, [isDarkTheme])

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setIsDarkTheme(true);

    const handleChange = (event: MediaQueryListEvent) => setIsDarkTheme(event.matches);
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [])

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
        title="Problem"
        centered
        open={modalOpen}
        onOk={() => setModalOpen(false)}
        onCancel={() => setModalOpen(false)}
        footer={null}
      >
        <p>
          There was an issue, please try again later.
        </p>

      </Modal>
    );
  }

  const startTour = () => {
    setTourKey(prevKey => prevKey + 1);
    setTourOpen(true);
    setInfoModalOpen(false);
    console.log(tourKey);
  }

  const { darkAlgorithm, defaultAlgorithm } = theme

  const lightTheme = {
    algorithm: defaultAlgorithm,
    token: {
      colorPrimary: "#F7996E",
      colorBgLayout: "#FFFFFF",
      colorLink: "#F7996E",
      colorLinkHover: "#F7996E",
      colorSplit: "#F7996E",
    }
  }

  const darkTheme = {
    algorithm: darkAlgorithm,
    token: {
      colorPrimary: "#4A7C59",
      colorBgLayout: "#141414",
      colorLink: "#4A7C59",
      colorLinkHover: "#4A7C59",
      colorLinkActive: "#4A7C59",
      colorSplit: "#4A7C59",
    }
  }

  return (
    <ConfigProvider
      theme={isDarkTheme ? darkTheme : lightTheme}
    >
      <div
        style={{
          width: '100vw',
          height: '100vh',
          backgroundColor: isDarkTheme ? darkTheme.token.colorBgLayout : lightTheme.token.colorBgLayout,
          transition: 'background-color 0.3s ease'
        }}
      >
        <Modal
          title="Welcome"
          centered
          open={infoModalOpen}
          onOk={() => setInfoModalOpen(false)}
          onCancel={() => setInfoModalOpen(false)}
          // footer={
          //   tourKey < 1
          //     ?
          //     [<Button
          //       key='tour-button'
          //       type="primary"
          //       onClick={startTour}
          //     >
          //       Begin Tour
          //     </Button>
          //     ] : null}
          footer={null}
        >
          <p>
            Thanks for checking out this site. It's still a work in progress and I'm aware of some of the issues with the board models.
          </p>
          <p>
            If you come across any bugs - or just have feedback or suggestions - please open an issue in the <a target="_blank" rel='noreferrer' href="https://github.com/MattReisdorf/RideRender/issues">GitHub</a> repo. I'll take a look and try to get it fixed.
          </p>

          <p>
            The plan is to have all of the boards available from Evo on here, but I'm currently only through GNU. New boards will be added periodically as I get them finished.
          </p>

          <Divider />

          <p>
            - Matt
          </p>

        </Modal>
        <Button
          type='text'
          className='openInfoButton'
          onClick={() => setInfoModalOpen(true)}
          ref={infoRef}
        >

          {
            isDarkTheme
              ?
              <InfoCircleFilled
                style={{
                  color: '#4A7C59',
                  fontSize: '20px',
                  transition: 'color 0.3s'
                }}
              />
              :
              <InfoCircleFilled
                style={{
                  color: '#F7996E',
                  fontSize: '20px',
                  transition: 'color 0.3s'
                }}
              />
          }
        </Button>

        <Button
          type='text'
          className='themeControls'
          onClick={() => {
            setIsDarkTheme(!isDarkTheme);
          }}
          style={{
            position: 'fixed',
            top: '20px',
            left: '9px',
            zIndex: '1000'
          }}
          ref={themeRef}
        >

          <SunFilled
            className={`${isDarkTheme ? 'fade-out' : 'fade-in'}`}
            style={{
              color: '#F7996E',
              fontSize: '20px',
              transition: 'opacity 0.3s ease'
            }}
          />
          <MoonFilled
            className={`${isDarkTheme ? 'fade-in' : 'fade-out'}`}
            style={{
              color: '#4A7C59',
              fontSize: '20px',
              transition: 'opacity 0.3s ease',
              position: 'absolute'
            }}
          />
        </Button>

        <Button
          className={`closedBrandDrawerButton ${brandDrawerOpen ? 'openedBrandDrawerButton' : ''
            } ${boardDrawerOpen ? 'hidden' : ''}`}
          type="text"
          onClick={openBrandDrawer}
          ref={buttonRef}
          style={{
            fontSize: '20px'
          }}
        >
          {
            isDarkTheme
              ?
              <DoubleLeftOutlined
                style={{
                  color: '#4A7C59',
                  fontSize: '20px',
                  transition: 'color 0.3s'
                }}
              />
              :
              <DoubleLeftOutlined
                style={{
                  color: '#F7996E',
                  fontSize: '20px',
                  transition: 'color 0.3s'
                }}
              />
          }
        </Button>

        <Drawer
          title={
            <div style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', height: '65px' }}>
              Brand
            </div>
          }
          placement="right"
          onClose={handleCloseBrandDrawer}
          open={brandDrawerOpen}
          closable={
            windowWidth <= 440 ? true : false
          }
          width={
            windowWidth <= 440 ? windowWidth : 378
          }
          className="brandDrawer"
          style={{
          }}
        >
          {Object.keys(boards).map((brand: string, index: number) => (
            <Button
              className="brandDrawerButton"
              key={index}
              type="link"
              onClick={() => handleBrandSelect(brand)}

            >
              <img className={`logoButton ${brand}`} src={`/images/logos/${brand}-${lightOrDark}.png`} alt={brand} ref={brandRef} />
            </Button>
          ))}

          <Drawer
            title={
              draftBrand ? (
                <img className="selectedBrandLogo" src={`/images/logos/${draftBrand}-${lightOrDark}.png`} alt={draftBrand} />
              ) : (
                ''
              )
            }
            placement="right"
            onClose={handleCloseBoardDrawer}
            open={boardDrawerOpen}
            closable={
              windowWidth <= 440 ? true : false
            }
            width={
              windowWidth <= 440 ? windowWidth : 378
            }
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
                        className={`boardButton ${boardData.name.toLowerCase()}`}
                        src={
                          draftBrand === 'Yes'
                            ? `/images/mens/${draftBrand}/${draftBrand.replace(/ /g, '-')}.--${boardData.name.replace(/ /g, '-')}.png`
                            : `/images/mens/${draftBrand}/${boardData.name}.png`
                        }
                        alt={`${draftBrand} ${boardData.name}`}
                        ref={boardRef}
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

        {/* <Tour key={tourKey} mask={false} type="primary" open={tourOpen} onClose={() => setTourOpen(false)} steps={steps} zIndex={2000} /> */}

        {confirmedBrand && confirmedBoard && (
          <>
            <BoardInfo board={confirmedBoard} brand={confirmedBrand} boardData={boards} isDarkTheme={isDarkTheme} />
            <div className="imageContainer" ref={modelRef}>
              <ModelRender brand={confirmedBrand} board={confirmedBoard} boardData={boards} isDarkTheme={isDarkTheme} />
            </div>
          </>
        )}
      </div>
    </ConfigProvider>
  );
}