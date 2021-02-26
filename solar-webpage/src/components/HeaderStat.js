import React from 'react';
import {  Grid } from '@material-ui/core';


export default function Layout(props) {
    const { fieldName, fieldVal } = props;

    return (
        <Grid item>
            <Grid item>
                {fieldName}
            </Grid>
            <Grid item>
                {fieldVal}
            </Grid>
            
        </Grid>
    );
}