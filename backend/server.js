const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const cors = require("cors");
require("dotenv").config();
const port = process.env.NODE_PORT;
const { getHypeFromDict, getTimeStamp } = require("./score");
const morgan = require("morgan");

app.use(
  morgan("short", {
    skip: (req, res) => {
      return req.originalUrl.startsWith("/receive-");
    },
  })
);

app.use(bodyParser.json());
app.use(
  cors({
    origin: ["http://localhost:3000"],
  })
);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

const { Collection_Anal, TimeSeries } = require("./database");
app.use(bodyParser.json());
app.use(cors());

app.post("/load-sentiment-by-tag", async (req, res) => {
  const tag = req.body.tag;
  console.log("The sentiment tag is: ", tag);
  const nfts = await Collection_Anal.find({ tag: tag }).catch((error) => {
    console.log("Error in finding sentiment for tag " + tag + ". " + error);
    res.sendStatus(500);
  });
  res.send(nfts);
});

app.post("/load-collection-time-series", async (req, res) => {
  const name = req.body.name;

  const timeSeries = await TimeSeries.find({ name: name }).catch((error) => {
    console.log("Error in finding name for time series" + tag + ". " + error);
    res.sendStatus(500);
  });
  timeSeries.sort((a, b) => {
    getTimeStamp(a["createdAt"]) - getTimeStamp(b["createdAt"]);
  });

  const hypes = timeSeries.map((dict) => getHypeFromDict(dict));
  const followers = timeSeries.map((dict) => dict["twitter_followers_count"]);
  const positives = timeSeries.map((dict) => dict["twitter_sent_avg_positive"]);
  const neutrals = timeSeries.map((dict) => dict["twitter_sent_avg_neutral"]);
  const negatives = timeSeries.map((dict) => dict["twitter_sent_avg_negative"]);
  const floorPrices = timeSeries.map((dict) => dict["_doc"]["floorPrice"]);

  const volume24h = timeSeries.map((dict) => dict["_doc"]["volume24h"]);
  const volumeAll = timeSeries.map((dict) => dict["_doc"]["volumeAll"]);
  const listedCount = timeSeries.map((dict) => dict["_doc"]["listedCount"]);

  const norms = timeSeries.map((dict) => dict["twitter_sent_avg_norm"]);
  const dateTime = timeSeries.map((dict) => getTimeStamp(dict["createdAt"]));

  const data = {
    dateTime: dateTime,
    hype: hypes,
    follower: followers,
    positive: positives,
    neutral: neutrals,
    negative: negatives,
    norm: norms,
    floorPrice: floorPrices,
    volume24h: volume24h,
    volumeAll: volumeAll,
    listedCount: listedCount,
  };

  res.send(data);
});
