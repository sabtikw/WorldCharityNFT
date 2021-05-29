import { Menu } from "semantic-ui-react";
import WorldPeace from "../build/contracts/WorldPeace.json";
import map from "../build/deployments/map.json";
import { BigNumber, ethers } from "ethers";
import { useState } from "react";


function AccountAddress() {
   // store greeting in local state
   const [currentAddress, setCurrentAddress] = useState("Click to Connect");

   
   // request access to the user's MetaMask account
   async function requestAccount() {
     await window.ethereum.request({ method: "eth_requestAccounts" });
   }
 



   // call the smart contract, read the current greeting value
   async function fetchAddress() {
    requestAccount()

     if (typeof window.ethereum !== "undefined") {


       const provider = new ethers.providers.Web3Provider(window.ethereum);
       const signer = await provider.getSigner();
       try {
       const signerAddress = await signer.getAddress();
       
       setCurrentAddress("Account:".concat(signerAddress));
       } catch (err) {

       }
     }
   }
 
   // call the smart contract, send an update
   
 window.ethereum.on('accountsChanged', function (accounts) {
  fetchAddress()
})
   return (
    <Menu.Item position='right' 
              name={currentAddress}
              
              onClick={fetchAddress}
            />
    
    
   );
 }
 
 



export default AccountAddress;
