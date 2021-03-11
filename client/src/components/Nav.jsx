import React from 'react';
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';

import './Nav.css';

const Nav = () => {
    
  return (
    <Menu right disableAutoFocus noOverlay>
      <Link className="menu-item" to="/" style={{textDecoration: 'none'}}>
        Home
      </Link>
      <Link className="menu-item" to="/Estimator" style={{textDecoration: 'none'}}>
        Estimator
      </Link>
      <Link className="menu-item" to="/" style={{textDecoration: 'none'}}>
        About
      </Link>
    </Menu>
  );
};

export default Nav;