import React, { useEffect, useState } from 'react';
import '../../css/Header.css';
import { useHistory } from 'react-router-dom';
import { Box, TextField, Autocomplete } from '@mui/material';
import { AuthContext } from '../../App';
import HomeIcon from '@mui/icons-material/Home';

const Header = () => {

    const { state } = React.useContext(AuthContext);

    const [data, setData] = useState([]);

    const history = useHistory();

    const handleSearch = (newValue) => {
        history.push(`/details/${newValue.name}`)};

    const directToHome = () => {
        history.push(`/`)
    }

    useEffect(() => {

        if (state.sentimentBoardAllTrending) {
            let allCollections = [].concat(state.sentimentBoardAllTrending)
            setData(allCollections)
        }

    }, [state.sentimentBoardAllTrending])

    return (
        <div className="header">
            <div onClick={directToHome} className="item"><HomeIcon /> Home</div>

            <Autocomplete
                loading={data.length === 0}
                id="searchCollection"
                options={data}
                autoComplete
                autoHighlight
                style={{ backgroundColor: "#1c1f26", width: "100%", borderRadius: "2em" }}
                onChange={(event, newValue) => {
                    if (newValue) {
                        handleSearch(newValue);
                    }
                }}
                getOptionLabel={(option) => option.name}
                renderOption={(props, option) => (
                    <Box component="li" sx={{ '& > img': { mr: 2, flexShrink: 0 } }} {...props} key={option._id}>
                        <img
                            loading="lazy"
                            width="20"
                            src={option.image}
                            srcSet={`${option.image} 2x`}
                            alt=""
                        />
                        {option.name}
                    </Box>
                )}
                renderInput={(params) => (
                    <TextField
                        sx={{ input: { color: 'white' } }}
                        {...params}
                        label="🔍 Search Collections"
                        InputLabelProps={{
                            style: { color: '#A8B3CF' },
                        }}
                        inputProps={{
                            ...params.inputProps,
                            autoComplete: 'new-password',
                            form: {
                                autocomplete: 'off',
                            },
                            border: 'none'
                        }}
                    />
                )}
            />
        </div>
    );
};

export default Header;
