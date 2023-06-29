// Connect to mongoDB
const mongoose = require("mongoose");
require("dotenv").config();

var connectionToNFTDashboard = mongoose.createConnection(
  process.env.MONGOOSE_ADDRESS_NFT_DASHBOARD,
  { useNewUrlParser: true },
  function (err) {
    if (err) {
      throw err;
    }
    console.log("Connected to NFT Dashboards!");
  }
);

const twitterCollectionSchema = mongoose.Schema(
  {
    description: String,
    discord: String,
    image: String,
    name: String,
    symbol: String,
    tag: String,
    twitter: String,
    twitter_avg_likes: Number,
    twitter_avg_quote: Number,
    twitter_avg_reply: Number,
    twitter_avg_retweet: Number,
    twitter_emo_avg_anger: Number,
    twitter_emo_avg_joy: Number,
    twitter_emo_avg_optimism: Number,
    twitter_emo_avg_sadness: Number,
    twitter_emo_std_anger: Number,
    twitter_emo_std_joy: Number,
    twitter_emo_std_optimism: Number,
    twitter_emo_std_sadness: Number,
    twitter_followers_count: Number,
    twitter_following_count: Number,
    twitter_listed_count: Number,
    twitter_sent_avg_negative: Number,
    twitter_sent_avg_neutral: Number,
    twitter_sent_avg_norm: Number,
    twitter_sent_avg_positive: Number,
    twitter_sent_std_negative: Number,
    twitter_sent_std_neutral: Number,
    twitter_sent_std_norm: Number,
    twitter_sent_std_positive: Number,
    twitter_tweet_count: Number,
  },
  { collection: "collection_anal" }
);

const timeSeries = mongoose.Schema(
  {
    name: String,
    twitter: String,
    discord: String,
    description: String,
    image: String,
    symbol: String,
    tag: String,
    createdAt: String,
    __v: Number,
    twitter_avg_likes: Number,
    twitter_avg_reply: Number,
    twitter_avg_quote: Number,
    twitter_avg_retweet: Number,
    twitter_scam_tweets: Array,
    twitter_sent_avg_negative: Number,
    twitter_sent_std_negative: Number,
    twitter_sent_avg_neutral: Number,
    twitter_sent_std_neutral: Number,
    twitter_sent_avg_positive: Number,
    twitter_sent_std_positive: Number,
    twitter_sent_avg_norm: Number,
    twitter_sent_std_norm: Number,
    twitter_emo_avg_anger: Number,
    twitter_emo_std_anger: Number,
    twitter_emo_avg_joy: Number,
    twitter_emo_std_joy: Number,
    twitter_emo_avg_optimism: Number,
    twitter_emo_std_optimism: Number,
    twitter_emo_avg_sadness: Number,
    twitter_emo_std_sadness: Number,
    twitter_followers_count: Number,
    twitter_following_count: Number,
    twitter_tweet_count: Number,
    twitter_listed_count: Number,
  },
  { collection: "time_series" }
);

const TimeSeries = connectionToNFTDashboard.model(
  "TimeSeries",
  timeSeries,
  "time_series"
);
const Collection_Anal = connectionToNFTDashboard.model(
  "Collection_Anal",
  twitterCollectionSchema,
  "collection_anal"
);

module.exports = { Collection_Anal, TimeSeries };
