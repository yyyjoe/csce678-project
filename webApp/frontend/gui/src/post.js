import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
// import clsx from 'clsx';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
// import Collapse from '@material-ui/core/Collapse';
// import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import { red } from '@material-ui/core/colors';
import FavoriteIcon from '@material-ui/icons/Favorite';
// import ShareIcon from '@material-ui/icons/Share';
// import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
// import MoreVertIcon from '@material-ui/icons/MoreVert';

const useStyles = makeStyles(theme => ({
    card: {
      maxWidth: "32%",
      marginTop: 10,
      marginLeft: "1%"
    },
    media: {
      width: "100%",
      paddingTop: '56.25%', // 16:9
    },
    expand: {
      transform: 'rotate(0deg)',
      marginLeft: 'auto',
      transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
      }),
    },
    expandOpen: {
      transform: 'rotate(180deg)',
    },
    avatar: {
      backgroundColor: red[500],
    },
    content: {
      // height : 120,
    }
  }));

export default function RecipeReviewCard({userID, date, imgURL, text, like}) {
    const classes = useStyles();
    // const [expanded, setExpanded] = React.useState(false);
  
    // const handleExpandClick = () => {
    //   setExpanded(!expanded);
    // };
  
    return (
      <Card className={classes.card}>
        <CardHeader
          // avatar={
          //   <Avatar aria-label="recipe" className={classes.avatar}>
          //     {userID}
          //   </Avatar>
          // }
          // title={userID}
          // subheader={date}
        />
        <CardMedia
          className={classes.media}
          image={imgURL}
          title=""
        />
        <CardActions disableSpacing>
          <IconButton aria-label="add to favorites" disabled={true}>
            <FavoriteIcon />
            <Typography variant="body2" color="textSecondary" component="p">
            {like}
          </Typography>
          </IconButton>
        </CardActions>
        <CardContent className={classes.content}>
          <Typography variant="body2" color="textSecondary" component="p">
            {text}
          </Typography>
        </CardContent>
      </Card>
    );
  }