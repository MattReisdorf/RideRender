import { DoubleRightOutlined } from '@ant-design/icons';
import { Button, Card, Col, Descriptions, DescriptionsProps, Drawer, Row, Space } from 'antd';
import React, { useState, useEffect } from 'react';

import '../styles/antdOverrides.css'


interface ModelRenderProps {
  brand: string | null,
  board: string | null,
  boardData: BoardsData
}

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

export const BoardInfo: React.FC<ModelRenderProps> = ({ brand, board, boardData}) => {

  const [infoDrawerOpen, setInfoDrawerOpen] = useState<boolean>(false);
  const [windowWidth, setWindowWidth] = useState<number>(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleInfoDrawer = () => {
    setInfoDrawerOpen(!infoDrawerOpen);
  }

  if (brand && board) {
    const brandArray = boardData[brand]

    const foundItem = brandArray.find((item) => {
      const [key] = Object.keys(item);
      return item[key].name === board;
    })

    if (!foundItem) {
      return (
        null
      )
    }
    const [foundKey] = Object.keys(foundItem);
    const matchedBoard = foundItem[foundKey];

    const descriptions: DescriptionsProps['items'] = [
      {
        key: '1',
        label: 'Sizes',
        children: <p>{matchedBoard.sizes.join(', ').toUpperCase()}</p>,
        span: 3
      },
      {
        key: '2',
        label: 'Shape',
        children: <p>{matchedBoard["Shape:"]}</p>,
        span: 3
      },
      {
        key: '3',
        label: 'Rocker Type',
        children: <p>{matchedBoard["Rocker Type:"]}</p>,
        span: 3
      },
      {
        key: '4',
        label: 'Flex Rating',
        children: <p>{matchedBoard["Flex Rating:"]}</p>,
        span: 3
      },
      {
        key: '5',
        label: 'Terrain',
        children: <p>{matchedBoard["Terrain:"]}</p>,
        span: 3
      },
      {
        key: '6',
        label: 'Binding Mount Pattern',
        children: <p>{matchedBoard["Binding Mount Pattern:"]}</p>,
        span: 3
      },
      {
        key: '7',
        label: 'Ability Level',
        children: <p>{matchedBoard["Ability Level:"]}</p>,
        span: 3
      },
    ]


    return (
      <>
        <Button
          className='boardInfoButton'
          type='text'
          onClick={handleInfoDrawer}
          // icon={<DoubleRightOutlined />}
          iconPosition='end'
          style={{
            position: 'fixed',
            top: '20px',
            left: '9px'
          }}
        >
          More Info
        </Button>
        <Drawer
          title = {
            <div style = {{width: '100%', textAlign: 'center',}}>
              {matchedBoard.name.replace(/-/g, " ").replace(/\b[a-z]/g, match => match.toUpperCase())} - {matchedBoard.price}
            </div>
          }
          placement='left'
          onClose={handleInfoDrawer}
          open={infoDrawerOpen}
          closable={
            windowWidth <= 440 ? true : false
          }
          width={
            windowWidth <= 440 ? windowWidth : 378
          }
          footer= {[
            <a href = {matchedBoard.link} target = "_blank">
              <Button block>
                Check This Board Out On Evo
              </Button>
            </a>
          ]}
        >

          <Descriptions bordered items = {descriptions} />

          {/* <div
            style = {{
              marginTop: '-200px'
            }}
          >
            <a href = {matchedBoard.link} target = "_blank">
              <Button block>
                Check This Board Out On Evo
              </Button>
            </a>
          </div> */}
        </Drawer>
      </>
    )
  }

  return null
}