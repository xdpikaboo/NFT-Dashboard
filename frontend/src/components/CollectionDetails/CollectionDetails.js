import React, { useEffect, useState } from 'react';
import { Grid } from '@material-ui/core';
import axios from "axios";
import TradingViewChart from "../Graph/TradingViewChart";
import { round } from '../../helper/utils';
import InfoCard from '../Headers/InfoCard';
import { AuthContext } from "../../App";
import { FaTwitter, FaDiscord, } from "react-icons/fa";
import LanguageIcon from '@mui/icons-material/Language';
import magicedenicon from '../../assets/magicedenicon.png';
import IconButton from '@mui/material/IconButton';
import CircleIcon from '@mui/icons-material/Circle';
import Loading from '../Loading/Loading';
import PieChart from '../Graph/PieChart';
import MenuItem from '@mui/material/MenuItem';
import { FormControl, Select } from '@material-ui/core';

const CollectionDetails = (props) => {

    const { state } = React.useContext(AuthContext);
    const [timeSeries, setTimeSeries] = React.useState(null);

    const [name] = useState(props.match.params.collectionName)

    const [emotion_pos, setEmotion_pos] = useState(null)
    const [emotion_sadness, setEmotion_sadness] = useState(null)
    const [emotion_anger, setEmotion_anger] = useState(null)
    const [pos, setPos] = useState(null)
    const [neu, setNeu] = useState(null)
    const [neg, setNeg] = useState(null)
    const [img, setImg] = useState(null)
    const [collectionDescription, setCollectionDescription] = useState(null)
    const [shock, setShock] = useState(null)
    const [me, setMe] = useState(null)
    const [website, setWebsite] = useState(null)
    const [twitter, setTwitter] = useState(null)
    const [discord, setDiscord] = useState(null)

    const [chartType, setChartType] = useState("Sentiment");

    const handleChangeType = (event) => {
        setChartType(event.target.value);
    }

    const getTwitterTimeSeriesData = async (name) => {
        const url = process.env.REACT_APP_BACKEND + "/load-collection-time-series"
        const timeSeriesData = (await axios.post(url, { "name": name })).data
        setTimeSeries(timeSeriesData)
    }

    useEffect(() => {
        if (name) {
            getTwitterTimeSeriesData(name);
        }
    }, [name])

    useEffect(() => {
        if (state.sentimentBoardAllTrending) {

            let collections = [].concat(state.sentimentBoardAllTrending)

            let collection = collections.find(c => c.name === name);

            let negData = (collection?.twitter_sent_avg_negative * 100);
            let neuData = (collection?.twitter_sent_avg_neutral * 100);
            let posData = (collection?.twitter_sent_avg_positive * 100);

            setPos(posData);
            setNeu(neuData);
            setNeg(negData);

            setCollectionDescription(collection?.description)

            let twitter_emo_avg_anger = collection?.twitter_emo_avg_anger
            let twitter_emo_avg_joy = collection?.twitter_emo_avg_joy
            let twitter_emo_avg_optimism = collection?.twitter_emo_avg_optimism
            let twitter_emo_avg_sadness = collection?.twitter_emo_avg_sadness

            let emotion_posData = ((twitter_emo_avg_joy + twitter_emo_avg_optimism) * 100);
            twitter_emo_avg_anger = (twitter_emo_avg_anger * 100);
            twitter_emo_avg_sadness = (twitter_emo_avg_sadness * 100);

            setEmotion_pos(emotion_posData)
            setEmotion_sadness(twitter_emo_avg_sadness)
            setEmotion_anger(twitter_emo_avg_anger)

            setImg(collection?.image)
            setShock(collection?.shock)

            setMe(`https://magiceden.io/marketplace/${collection?.symbol}`)
            setTwitter(collection?.twitter)
            setDiscord(collection?.discord)
            setWebsite(collection?.website)
        }
        // eslint-disable-next-line
    }, [name, state.sentimentBoardAllTrending])

    const latestValue = (array) => {
        return array[array.length - 1]
    }

    return (
        <div style={{ color: "white", marginBottom: "7vh" }}>

            <Grid spacing={1} container>
                <Grid xs={3} item>
                    <img style={{ width: "13vw", height: "auto", borderRadius: "50%" }} src={img} alt="" />
                </Grid>
                <Grid xs={4} item style={{ marginRight: "4vw" }}>
                    <div style={{ fontSize: "35px", marginBottom: "1vh" }}>{name}</div>
                    <div style={{ fontSize: "22px", color: "grey", marginBottom: "1vh" }}>{collectionDescription}</div>
                    <div>
                        {me && <IconButton onClick={() => window.open(me, "_blank")} color="secondary">
                            <img alt="ME" src={magicedenicon} style={{ width: "50px" }} />
                        </IconButton>}
                        {website && <IconButton onClick={() => window.open(website, "_blank")} style={{ color: "white" }}>
                            <LanguageIcon style={{ width: "50px" }} />
                        </IconButton>}
                        {twitter && <IconButton onClick={() => window.open(twitter, "_blank")} style={{ color: "#1DA1F2" }}>
                            <FaTwitter style={{ width: "50px" }} />
                        </IconButton>}
                        {discord && <IconButton onClick={() => window.open(discord, "_blank")} style={{ color: "#5865F2" }}>
                            <FaDiscord style={{ width: "50px" }} />
                        </IconButton>}
                    </div>
                </Grid>
                <Grid xs={4} item>
                    {timeSeries !== undefined && timeSeries !== null && shock !== null && Object.keys(timeSeries).length !== 0 && <InfoCard
                        floorPrice={round(latestValue(timeSeries.floorPrice))}
                        volume24h={round(latestValue(timeSeries.volume24h))}
                        volumeAll={round(latestValue(timeSeries.volumeAll))}
                        listCount={latestValue(timeSeries.listedCount)}
                        shock={shock}
                    />}
                </Grid>
                <Grid xs={12} item>
                    {timeSeries === null && <Loading />}
                    {timeSeries !== undefined && timeSeries !== null && shock !== null && Object.keys(timeSeries).length !== 0 && <Grid style={{ marginLeft: "2vw" }} container>
                        <Grid container>
                            <Grid xs={8} item>
                                <TradingViewChart name={name} time={timeSeries.dateTime} value={timeSeries.norm.map((x) => x * 100)} value2={timeSeries.floorPrice} value3={timeSeries.listedCount} addListedCount={true} title="Sentiment vs Floor Price vs Listed Count Chart" isNormalized={true} />

                                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-evenly" }}>
                                    <div style={{ display: "flex", alignItems: "center" }}>
                                        <CircleIcon style={{ color: "#394990", marginRight: "0.25vw" }} />
                                        <div>Sentiment</div>
                                    </div>
                                    <div style={{ display: "flex", alignItems: "center" }}>
                                        <CircleIcon style={{ color: "#46acb7", marginRight: "0.25vw" }} />
                                        <div>Floor price</div>
                                    </div>
                                    <div style={{ display: "flex", alignItems: "center" }}>
                                        <CircleIcon style={{ color: "#fd3c99", marginRight: "0.25vw" }} />
                                        <div>Listed Count</div>
                                    </div>
                                </div>

                            </Grid>

                            <Grid xs={4} item>
                                {chartType === "Sentiment" ? <PieChart isSentiment={true} positive={pos} neutral={neu} negative={neg} /> :
                                    <PieChart isSentiment={false} positive={emotion_pos} neutral={emotion_sadness} negative={emotion_anger} />
                                }
                                <div style={{ display: "flex", alignItems: "center", color: '#A8B3CF' }}>
                                    Chart type:
                                    <div>
                                        <FormControl sx={{ m: 1, width: 200 }}>
                                            <Select
                                                style={{ marginLeft: "1vw", color: "white", borderWidth: 0, borderRadius: "2em", backgroundColor: "#1c1f26", width: "100%" }}
                                                id="chartType"
                                                value={chartType}
                                                onChange={handleChangeType}
                                            >
                                                <MenuItem key={1} value={"Sentiment"}>Sentimental Analysis</MenuItem>
                                                <MenuItem key={2} value={"Mood"}>Mood</MenuItem>
                                            </Select>
                                        </FormControl>
                                    </div>
                                </div>
                            </Grid>
                        </Grid>
                    </Grid>}
                </Grid>
            </Grid>
        </div>
    )
};

export default CollectionDetails;
