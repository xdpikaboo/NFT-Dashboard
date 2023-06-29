import React, { useState } from 'react';
import "../../css/Header.css";
import { Link } from 'react-router-dom';
import { Box, List, ListItem, ListItemIcon, makeStyles } from '@material-ui/core';
import HomeIcon from '@mui/icons-material/Home';

const useStyles = makeStyles(theme => ({
  root: {
    width: '14vw',
    minWidth: '14vw',
    borderRight: '1px solid rgba(145, 158, 171, 0.24)',
    height: '100vh',
    top: 0,
    position: 'sticky',
    backgroundColor: '#0e1217',
  },
  navItem: {
    paddingLeft: '2vw',
    marginBottom: '1vh',
    height: '5vh',
    color: '#A8B3CF',
    "&:hover": {
      color: "white"
    }
  },
  navItemActive: {
    paddingLeft: '2vw',
    marginBottom: '1vh',
    height: '5vh',
    backgroundColor: 'rgba(0, 171, 85, 0.08)',
    color: 'white',
    fontWeight: 'bold',
    '&::before': {
      width: '0.1vw',
      position: 'absolute',
      content: '""',
      top: 0,
      bottom: 0,
      right: 0,
      backgroundColor: 'white',
    },
    "&:hover": {
      color: "#A8B3CF"
    }
  },
  navItemIcon: {
    minWidth: '2.5vw',
    color: "white"
  },
  butArea: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    color: '#A8B3CF'
  },
}));

function Navbar() {
  const classes = useStyles();

  const generateActiveTab = (pathname) => {
    if (pathname === "/new-collections") return "New Releases"
    else if (pathname === "/alltrending") return "Trending"
    else if (pathname === "/1h") return "1h"
    else if (pathname === "/1day") return "24h"
    else if (pathname === "/7days") return "7 Days"
    else return "All Collections"
  }

  const [activeTab, setActiveTab] = useState(() => generateActiveTab(window.location.pathname))

  const navList = [
    {
      label: 'Home',
      path: '/all',
      icon: (<HomeIcon />),
    },
  ];

  return (
    <>
    {<Box className={classes.root}>
      <List style={{marginTop: "5vh"}}>
        {navList.map(nav => {
          return <ListItem
            key={nav['label']}
            className={activeTab === nav['label'] ? classes.navItemActive : classes.navItem}
            button component={Link}
            to={nav['path']}
            onClick={() => setActiveTab(nav['label'])}
          >
            <ListItemIcon className={classes.navItemIcon}>
              {nav['icon']}
            </ListItemIcon>
            {nav['label']}
          </ListItem>

        })}
      </List>

      <Box className={classes.butArea}>
        <div>© 2022: CWRU</div>
      </Box>

    </Box>}
    </>
  );
}

export default Navbar;