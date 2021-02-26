import React, { useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Container, Grid, List, ListItem, ListItemText } from '@material-ui/core';
import ListItemLink from './ListItemLink';
import HeaderStat from './HeaderStat';



export default function Layout(props) {
  const { children } = props;


  return (
      <Container>
        <Grid container direction="row" spacing={5}>
          <HeaderStat fieldName="Main Current" fieldVal={22.22} /> {/* putting static placeholders for now */}
          <HeaderStat fieldName="MPPT1" fieldVal={88.88} />
          <HeaderStat fieldName="MPPT1" fieldVal={99.99} />
          <HeaderStat fieldName="RPM" fieldVal={33.33} />
          <HeaderStat fieldName="Lowest Voltage" fieldVal={66.66} />
          <HeaderStat fieldName="Highest Temp" fieldVal={77.88} />
        </Grid>
        <Grid container direction="row">
          <Grid item>
            <Router>
              <List>
                <ListItemLink to="/" primary="Summary" />
                <ListItemLink to="/gps" primary="GPS" />
                <ListItemLink to="/batteries" primary="Batteries" />
                <ListItemLink to="/temps" primary="Temperatures" />
                <ListItem><ListItemText primary="Display the current time and date here, will do this later" /></ListItem>
              </List>
            </Router>
          </Grid>
          <Grid conitem>
            {children}
          </Grid>
        </Grid>
      </Container>
  );
}
