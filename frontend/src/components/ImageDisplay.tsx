import React, { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';

interface ImageDisplayProps {
    brand: string | null,
    board: string | null
}

export const ImageDisplay: React.FC<ImageDisplayProps> = ({brand, board}) => {

    const [manufacturer, setManufacturer] = useState<string | null>(null);
    const [model, setModel] = useState<string | null>(null);
    const [errorThrown, setErrorThrown] = useState<boolean>(false);

    useEffect(() => {
        const checkFileExists = async() => {
            try {
                const makeModel = {
                    brand: brand,
                    board: board
                };
                const response = await axios.post('http://127.0.0.1:8000/existence/', makeModel)
                if (response.data.imageExists) {
                    setManufacturer(brand);
                    setModel(board);
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
        checkFileExists();
    }, [brand, board]);

    const boardPath = (
        manufacturer === 'Yes'
        ?
        `/images/mens/${manufacturer}/${manufacturer?.replace(/ /g, '-')}.-${model?.replace(/ /g, '-')}.jpg`
        :
        `/images/mens/${manufacturer}/${manufacturer?.replace(/ /g, '-')}-${model?.replace(/ /g, '-')}.jpg`
    );

    if (errorThrown) {
        return (
            <div>
                <span>There was a problem getting the board image, please try again later</span>
            </div>
        );
    }
    else if (manufacturer && model) {
        return (
            <div>
                <img src = {boardPath} />
            </div>
        );
    };
    return (null);
}