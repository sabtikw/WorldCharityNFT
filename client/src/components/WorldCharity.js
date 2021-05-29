import { Header, Item, Container, Divider } from "semantic-ui-react";
import WPHome from "../api/WPHome"

function WorldCharity() {
  return (
    
<div>
   
    
        
<Container textAlign='center'>
      <Header as="h1">
        World Charity NFT with Liquid Stacking
        <Divider />
        <Container textAlign='justified'>
        <Header.Subheader>
          <Item.Group>
            <Item>
              <Item.Content>(NFT) Deposit ETH to earn Country Art</Item.Content>
            </Item>

            <Item>
              <Item.Content>
               (Liquid Staking) Deposited ETH is staked on Liquid Staking Platform 
              </Item.Content>
            </Item>

            <Item>
              <Item.Content>
                (Govern) NFT Owners vote to send staking rewards to Charity of
                their choosing
              </Item.Content>
            </Item>

            <Item>
              <Item.Content>
                (Transfer) 5% dedducted on each NFT transfer and sent to the
                staking pool
              </Item.Content>
            </Item>
          </Item.Group>
        </Header.Subheader>
        </Container>
      </Header>
      </Container>
      <Divider/>
      
      <Container>
          <WPHome />
      </Container>
      </div>
  );
}
export default WorldCharity;
