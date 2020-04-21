import React  from 'react';
import Grid from '@material-ui/core/Grid';
import RecipeReviewCard from './post'
import InstagramEmbed from 'react-instagram-embed';


export default (posts) => {
    // console.log(posts)
    return (
        <Grid container direction="column">
            {
                posts.posts.map(post => {
                    return (
                        // <RecipeReviewCard key={post.userID}
                        //     userID={post.userID}
                        //     date={post.date}
                        //     imgURL={post.imgURL}
                        //     text={post.text}
                        //     like={post.like}
                        // />
                        <InstagramEmbed
                            url='https://www.instagram.com/p/B-ky7fYp8RP/'
                            hideCaption={false}
                            containerTagName='div'
                            protocol=''
                            injectScript
                            onLoading={() => {}}
                            onSuccess={() => {}}
                            onAfterRender={() => {}}
                            onFailure={() => {}}
                        />
                    )
                })
            }
        </Grid>
    )
}