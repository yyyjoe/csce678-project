import React  from 'react';
import Grid from '@material-ui/core/Grid';
import RecipeReviewCard from './post'


export default (posts) => {
    // console.log(posts)
    return (
        <Grid container  style={{width : "100%"}}>
            {
                posts.posts.map(post => {
                    return (
                        <RecipeReviewCard key={post.userID}
                            userID={post.userID}
                            date={post.date}
                            imgURL={post.imgURL}
                            text={post.text}
                            like={post.like}
                        />
                    )
                })
            }
        </Grid>
    )
}