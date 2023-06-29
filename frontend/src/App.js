import React, { useEffect } from "react"
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import 'antd/dist/antd.css';
import { Box, makeStyles } from '@material-ui/core';
import axios from "axios";
import AllCollection from "./pages/AllCollection";
import CollectionDetails from "./components/CollectionDetails/CollectionDetails";
import Header from "./components/Headers/Header"

export const AuthContext = React.createContext();

const initialState = {
  sentimentBoardNewCollection: null,
  sentimentBoard1h: null,
  sentimentBoard1d: null,
  sentimentBoard7d: null,
  sentimentBoardAllTrending: null,
};

const reducer = (state, action) => {
  switch (action.type) {
    case "SET_SENTIMENT_BOARD_NEW_COLLECTION":
      return {
        ...state,
        sentimentBoardNewCollection: action.payload.sentimentBoardNewCollection
      }
    case "SET_SENTIMENT_BOARD_1H":
      return {
        ...state,
        sentimentBoard1h: action.payload.sentimentBoard1h
      }
    case "SET_SENTIMENT_BOARD_1D":
      return {
        ...state,
        sentimentBoard1d: action.payload.sentimentBoard1d
      }
    case "SET_SENTIMENT_BOARD_7D":
      return {
        ...state,
        sentimentBoard7d: action.payload.sentimentBoard7d
      }
    case "SET_SENTIMENT_BOARD_ALL_TRENDING":
      return {
        ...state,
        sentimentBoardAllTrending: action.payload.sentimentBoardAllTrending
      }
    default:
      return state;
  }
};

const useStyles = makeStyles(theme => ({
  content: {
    width: '100%',
    padding: '35px 50px 5px',
  }
}));

function App() {
  const [state, dispatch] = React.useReducer(reducer, initialState);

  const classes = useStyles();

  const getUniqueCollections = (collections) => {
    let collectionSet = new Set()
    let uniqueCol = []
    for (const collection of collections) {
      const name = collection.name ? collection.name : collection.collection_name
      if (!collectionSet.has(name)) {
        uniqueCol.push(collection)
        collectionSet.add(name)
      }
    }
    return uniqueCol
  }

  useEffect(() => {
    const path = `${process.env.REACT_APP_BACKEND}/load-sentiment-by-tag`

    axios.post(path, { "tag": "new-collections" }).then(results => {
      let data = results.data
      data.forEach(item => item.image = item.image.replace('nftstorage', 'dweb'))
      dispatch({
        type: "SET_SENTIMENT_BOARD_NEW_COLLECTION",
        payload: { sentimentBoardNewCollection: data }
      })
    })

    axios.post(path, { "tag": "popular-collections-1day" }).then(results => {
      let data = results.data
      data.forEach(item => item.image = item.image.replace('nftstorage', 'dweb'))
      dispatch({
        type: "SET_SENTIMENT_BOARD_1D",
        payload: { sentimentBoard1d: data }
      })
    })

    axios.post(path, { "tag": "popular-collections-7days" }).then(results => {
      let data = results.data
      data.forEach(item => item.image = item.image.replace('nftstorage', 'dweb'))
      dispatch({
        type: "SET_SENTIMENT_BOARD_7D",
        payload: { sentimentBoard7d: data }
      })
    })

    axios.post(path, { "tag": "popular-collections-1h" }).then(results => {
      let data = results.data
      data.forEach(item => item.image = item.image.replace('nftstorage', 'dweb'))
      dispatch({
        type: "SET_SENTIMENT_BOARD_1H",
        payload: { sentimentBoard1h: data }
      })
    })

  }, [])

  useEffect(() => {
    let allCollection = []
    if (state.sentimentBoardNewCollection && state.sentimentBoard1d && state.sentimentBoard7d && state.sentimentBoard1h) {
      allCollection = allCollection.concat(state.sentimentBoardNewCollection).concat(state.sentimentBoard1d).concat(state.sentimentBoard7d).concat(state.sentimentBoard1h)
      allCollection = getUniqueCollections(allCollection)
      dispatch({
        type: "SET_SENTIMENT_BOARD_ALL_TRENDING",
        payload: { sentimentBoardAllTrending: allCollection }
      })
    }

  }, [state.sentimentBoardNewCollection, state.sentimentBoard1h, state.sentimentBoard1d, state.sentimentBoard7d])

  return (
    <AuthContext.Provider
      value={{
        state,
        dispatch
      }}
    >
      <div className="App">
        <Router>
          <Box className={classes.content}>
            <Header />
            <Switch>
              <Route path="/details/:collectionName" render={(props) => { return <CollectionDetails {...props} key={window.location.pathname} /> }}>
              </Route>
              <Route path="/">
                <AllCollection />
              </Route>
            </Switch>
          </Box>
        </Router>
      </div>
    </AuthContext.Provider>
  );
}


export default App;
