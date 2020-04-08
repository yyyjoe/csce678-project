import React, { Component, Fragment } from 'react';
import { Button, TextField, Paper } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import PostList from './postList'
import Chart from './chart'
import Typography from '@material-ui/core/Typography';

const style = {
    PaperLeft: { padding: 10, marginTop: 10, marginBottom: 10, height: "100%", width : "100%" },
    PaperRight: { padding: 10, marginTop: 10, marginBottom: 10,  height: "100%", width : "100%" , overflow : 'auto'},
}

class MainFunction extends Component {

    render() {
        return (
            <Fragment>
                <Grid container direction="row" style={{width : "100%", height: "85%"}}>
                    <Grid container direction="column" style={{width : "29%", height: "100%"}}>
                        <Grid item style={{width : "100%"}}>
                            <Paper style={{ width : "95%", padding: 10, marginTop: 10, marginBottom: 10, height: "90%" }}>
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
                                    style={{ marginTop: 10, marginRight: 10 }}
                                    helperText={this.props.errorText}
                                />
                                <Button onClick={this.props.handleSend} variant="contained" style={{ marginTop: 10 }}>
                                    Go
                                </Button>
                            </Paper>
                        </Grid> 
                        <Grid item style={{width : "100%"}}>
                            <Paper style={{ padding: 10, marginTop: 20, marginBottom: 10, height: "100%", width : "95%"}}>
                                <Typography variant="subtitle2">
                                    Topic Percentage % : 
                                </Typography>
                                <Chart
                                    topics={this.props.topics}
                                />
                            </Paper>
                        </Grid>
                    </Grid>
                    <Grid container style={{width : "69%", height: "100%"}}>
                        <Paper style={style.PaperRight} >
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