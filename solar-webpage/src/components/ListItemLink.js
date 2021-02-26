// taken from https://material-ui.com/guides/composition/
// this doesn't seem to work at all...
import React from 'react';
import { Link } from 'react-router-dom';
import { ListItem, ListItemText } from '@material-ui/core';

export default function ListItemLink(props) {
    const { to, primary  } = props;
  
    const renderLink = React.useMemo(
      () => React.forwardRef((itemProps, ref) => <Link to={to} ref={ref} {...itemProps} />),
      [to],
    );
  
    return (
      <li>
        <ListItem button component={renderLink}>
          <ListItemText primary={primary}/>
        </ListItem>
      </li>
    );
  }