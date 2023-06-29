const rawHypeScore = (norm, twitterFollowers, twitterComments) => {
  const normScale = 0.2 * 1000 * 1;
  const twitterFollowerScale = 0.6;
  const twitterCommentScale = 0.2 * 1;
  const score =
    norm * normScale +
    twitterFollowers * twitterFollowerScale +
    twitterComments * twitterCommentScale;
  return score;
};

const sigmoid = (k, x0, x) => {
  return 1 / (1 + Math.exp(-k * (x - x0)));
};

const normalizeScore = (score) => {
  return sigmoid(4, 0.5, score / 10000);
};

const getHypeFromDict = (dict) => {
  const norm = dict["twitter_sent_avg_norm"];
  const twitterFollowers = dict["twitter_followers_count"];
  const twitterComments = dict["twitter_tweet_count"];

  const rawScore = rawHypeScore(norm, twitterFollowers, twitterComments);
  return normalizeScore(rawScore);
};

const getTimeStamp = (string) => {
  let dateTimeParts = string.split(" "),
    timeParts = dateTimeParts[1].split(":"),
    dateParts = dateTimeParts[0].split("-");

  let date = new Date(
    dateParts[0],
    parseInt(dateParts[1], 10) - 1,
    dateParts[2],
    timeParts[0],
    timeParts[1],
    timeParts[2]
  );

  return date.getTime();
};
module.exports = {
  rawHypeScore,
  sigmoid,
  normalizeScore,
  getHypeFromDict,
  getTimeStamp,
};
