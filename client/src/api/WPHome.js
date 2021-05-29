import { Message, Button, Progress } from "semantic-ui-react";
import WorldPeace from "../build/contracts/WorldPeace.json";
import LidoDemo from "../build/contracts/LidoDemo.json";
import map from "../build/deployments/map.json";
import { BigNumber, ethers } from "ethers";
import { useState, useEffect } from "react";

const WorldPeaceAddress = map.dev.WorldPeace[0];
const LidoDemoAddress = map.dev.LidoDemo[0];
function WPHome() {
  // store greeting in local state
  const [mintedTokens, setMintedTokens] = useState(0);
const [tokenCount, setTokenCount] = useState(0);
const [WPSharedPool, setWPSharedPool] = useState(0);
const [rewards, setRewards] = useState(0);
  // request access to the user's MetaMask account
  async function requestAccount() {
    await window.ethereum.request({ method: "eth_requestAccounts" });
  }

  // call the smart contract, read the current greeting value
  async function fetchTokenStatus() {
    if (typeof window.ethereum !== "undefined") {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const contract = new ethers.Contract(
        WorldPeaceAddress,
        WorldPeace.abi,
        provider
      );
      const LidoD = new ethers.Contract(
        LidoDemoAddress,
        LidoDemo.abi,
        provider
      );
      try {
        const  sharedpool = await contract.WPSharedPoolstkEthBalance();
        const mintedTokens_ = await contract.mintedWPTokens();
        const tokenCount_ = await contract.WP_TOKEN_COUNT();
       const rewards_ = await LidoD.balanceOf(WorldPeaceAddress);
        //console.log("data: ", mintedTokens_.toNumber());
        setMintedTokens(mintedTokens_);
        setTokenCount(tokenCount_);
        setWPSharedPool(sharedpool);
        setRewards(rewards_.sub(sharedpool))
        
      } catch (err) {
        console.log("Error: ", err);
      }
    }
  }

  // call the smart contract, send an update
  async function mintToken() {
    
    
    if (typeof window.ethereum !== "undefined") {
      await requestAccount();
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(WorldPeaceAddress, WorldPeace.abi, signer);
      const transaction = await contract.mint({value: ethers.utils.parseEther('2.0')});
      await transaction.wait();
      fetchTokenStatus();
    }
  }

  async function rebase() {
    
    
    if (typeof window.ethereum !== "undefined") {
      await requestAccount();
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(LidoDemoAddress, LidoDemo.abi, signer);
      const transaction = await contract.rebase(WorldPeaceAddress);
      await transaction.wait();
      fetchTokenStatus();
    }
  }
  
  
useEffect(() => {

  fetchTokenStatus();
}



);
  window.ethereum.on('connect', function (accounts) {
    fetchTokenStatus()
  })

  return (
    <div>


      <Message align='center'>Buy World Charity NFT</Message>
      <Progress value={mintedTokens.toString()} total={tokenCount.toString()} progress='ratio'><Button primary onClick={mintToken}>Buy NFT</Button></Progress>
      <Message>Shared Staked Charity Pool : {ethers.utils.formatEther(WPSharedPool)} stkETH</Message>
      <Message>Rewards Available for Charity : {ethers.utils.formatEther(rewards)}</Message>
      <Button primary onClick={rebase}>rebase to increase rewards(test)</Button>
      
      
    </div>
  );
}





export default WPHome;
