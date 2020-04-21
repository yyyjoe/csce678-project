import React, { Component, Fragment } from 'react';
import { Button, TextField, Paper } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import PostList from './postList'
import Chart from './chart'
import Typography from '@material-ui/core/Typography';

class MainFunction extends Component {

    render() {
        return (
            <Fragment>
                <Grid container direction="row" style={{height: "92%"}} justify="center">
                    <Grid container direction="column" style={{width: "20%"}}>
                        <Grid item style={{width: "100%"}}>
                            <Paper style={{width: "95%", padding: 10, marginTop: 10, marginBottom: 10, height: "90%" }}>
                                <Typography variant="subtitle2">
                                    Please Enter a public Instagram ID to get posts :
                                </Typography>
                                <TextField 
                                    error={this.props.isIdInvalid}
                                    id="user_id"
                                    placeholder="Your ID"
                                    value={this.props.userID}
                                    variant="outlined"
                                    onChange={this.props.handleChange}
                                    margin="normal"
                                    inputProps={{
                                        style: {fontSize: 15} 
                                    }}
                                    style={{ marginTop: 10, marginRight: 10}}
                                    helperText={this.props.errorText}
                                />
                                <Button onClick={this.props.handleSend} variant="contained" style={{ marginTop: 10 }}>
                                    Go
                                </Button>
                            </Paper>
                        </Grid> 
                        <Grid item style={{width: "100%"}}>
                            <Paper style={{ padding: 10, marginTop: 20, marginBottom: 10, height: "100%", width: "95%"}}>
                                <Typography variant="subtitle2">
                                    Topic Percentage % : 
                                </Typography>
                                <Chart
                                    topics={this.props.topics}
                                />
                            </Paper>
                        </Grid>
                    </Grid>
                    <Grid container style={{width : "670px", height: "100%", overflow: 'hide'}}>
                        <Paper style={{padding: 10, marginBottom: 10,  height: "100%", width: "100%", overflow: 'scroll'}}>
                            <PostList
                                posts={this.props.posts}
                            />
                        </Paper>
                    </Grid>
                </Grid>
            </Fragment>
        )
    }
}

export default MainFunction;