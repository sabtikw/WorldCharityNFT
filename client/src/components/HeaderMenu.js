import React, { Component } from 'react'
import { Input, Menu, Segment } from 'semantic-ui-react'
import { Link } from "react-router-dom";
import AccountAddress from "../api/AccountAddress"

export default class HeaderMenu extends Component {
    state = { activeItem: 'WorldCharity' }
  
    handleItemClick = (e, { name }) => this.setState({ activeItem: name })
  
    render() {
      const { activeItem } = this.state
      return (
        <div>
          <Menu pointing>
            <Menu.Item as={Link} to="/"
              name='World Charity'
              active={activeItem === 'WorldCharity'}
              onClick={this.handleItemClick}
            />
            <Menu.Item as={Link} to="rule"
              name='Dashboard'
              active={activeItem === 'rule'}
              onClick={this.handleItemClick}
            />
            <Menu.Item as={Link} to="govern"
              name='Govern'
              active={activeItem === 'govern'}
              onClick={this.handleItemClick}
            />
            <Menu.Item as={Link} to="transfer"
              name='Transfer'
              active={activeItem === 'govern'}
              onClick={this.handleItemClick}
            />
            <AccountAddress />
            
            
              
            
          </Menu>
         
          
        </div>
      )
    }
  }