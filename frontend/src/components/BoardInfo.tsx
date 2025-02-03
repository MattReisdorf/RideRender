import { Button, Card, Col, Row, Space } from 'antd';
import React from 'react';


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

export const BoardInfo: React.FC<ModelRenderProps> = ({ brand, board, boardData }) => {

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

    return (
      <div
        style = {{
          height: 'auto',
          width: 'auto',
          position: 'absolute',
          marginTop: '15px',
          marginLeft: '15px',
        }}
      >
        <Space direction="vertical" size={16}>
          <Card 
            title = {`${matchedBoard.name.replace(/-/g, " ").replace(/\b[a-z]/g, match => match.toUpperCase())} - ${matchedBoard.price}`}
            style = {{ 
              width: '30vw',
            }}
          >
          
            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Sizes:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard.sizes.join(', ')}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Shape:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Shape:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Rocker Type:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Rocker Type:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Flex Rating:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Flex Rating:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Terrain:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Terrain:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Binding Mount:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Binding Mount Pattern:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {8}>
                <p>Ability Level:</p>
              </Col>
              <Col span = {16}>
                <p>{matchedBoard["Ability Level:"]}</p>
              </Col>
            </Row>

            <Row gutter = {[24, 8]}>
              <Col span = {4} />
              <Col span = {16}>
                <a href = {matchedBoard.link}>
                  <Button block>
                    Check This Board Out On Evo
                  </Button>
                </a>
              </Col>
              <Col span = {4} />
            </Row>

          </Card>
        </Space>
      </div>
    )
  }
  
  return null
}