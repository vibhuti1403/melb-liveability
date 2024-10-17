import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles((theme) => ({
  root: {
    width: '20vw',
    height: '70vh',
    // maxWidth: '36ch',
    backgroundColor: theme.palette.background.paper,
  },
  inline: {
    display: 'inline',
  },
}));


function getcolor(sentiment){
  if(sentiment==="Negative")
  return "rgba(187, 0, 0, .4)"
  else if(sentiment==="Positive")
  return "rgba(43, 124, 43, .4)"
  else if(sentiment==="Neutral")
  return "rgba(231, 140, 7, .4)"
  else
  return "#ffffff";

}

const StreamTweets = () => {
  
  const classes = useStyles();

  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState([]);
    var config = {
    method: "get",
    url: process.env.REACT_APP_URL +"/realtime_tweets/_changes?heartbeat=1000&include_docs=true&limit=20&descending=true",
    headers: {
      Authorization: process.env.REACT_APP_USER,
    },
  };

  
  React.useEffect(() => {
    var axios = require("axios");

    const interval = setInterval(() => {
      setIsLoading(true)

      axios(config)
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => console.log(error));
      
    }, 30 * 1000);
  
    return () => clearInterval(interval);

    

  }, []);

  React.useEffect(() => {
    if (
      data.length !== 0) {
      setIsLoading(false);
    }
  }, [data]);

  return (

    <div>
      {isLoading ? (
       <h2>Real Time Tweets</h2>
      ) : (
        <div >
          <h2>Real Time Tweets</h2>

          <marquee direction="down" scrollamount="10">
          <List className={classes.root}>
          {data.results.map((d) => (
         

            <>
              <ListItem alignItems="flex-start" style={{backgroundColor: getcolor(d.doc.sentiment), borderRadius: "15px",marginBottom:'5px'}} >
                <ListItemAvatar>
                  <Avatar />
                </ListItemAvatar>
                <ListItemText
                  primary={d.doc.text}
                  secondary={
                    
                      <React.Fragment>
                      {"-" + d.doc.screen_name}
                      <br/>

                      <Typography
                        component="span"
                        variant="body2"
                        className={classes.inline}
                        color="textPrimary"
                      >
                        {d.doc.category}
                      </Typography>

                    </React.Fragment>
                  }
                />
              </ListItem>
              </>
           

          ))}

</List>
</marquee>

        </div>

      )}
    </div>


  );
}

export default StreamTweets
