//SPDX-License-Identifier: MIT

pragma solidity 0.8.4;

import '../interfaces/IERC20.sol';
import '../interfaces/library/SafeMath.sol';
import './ReentrancyGuard.sol';
import './AccessControl.sol';
import './Pausable.sol';

contract WPFinance is ReentrancyGuard, AccessControl, Pausable {
    using SafeMath for uint256;


    address internal CREATOR_ADDRESS; 
    address public  LIDO_FINANCE_CONTRACT_ADDRESS;
    uint256 public WPSharedPoolstkEthBalance; 
    bytes32 constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 constant DAO_ROLE = keccak256("DAO_ROLE");
    bytes32 constant OPERATION_ROLE = keccak256("OPERATION_ROLE");
    

    

    event LidoAccountChange(address indexed lidoaddress);
    event EthStakedToLido(uint256 indexed amount);
    event FundsWithdrawn(address indexed to, uint256 indexed amount);
    event FundsWithdrawnToCharity(address indexed to, uint256 indexed amount);

    constructor(address payable LIDO_FINANCE_CONTRACT_ADDRESS__,address payable CREATOR_ADDRESS__) {

        LIDO_FINANCE_CONTRACT_ADDRESS = LIDO_FINANCE_CONTRACT_ADDRESS__;
        CREATOR_ADDRESS = CREATOR_ADDRESS__;
    }


function pause() public onlyRole(OPERATION_ROLE) {

    _pause();
}


function resume() public onlyRole(OPERATION_ROLE) {

    _unpause();
}
function setLidoAccountAddress(address _LidoAccountAddress) public  onlyRole(OPERATION_ROLE){ //add access control

LIDO_FINANCE_CONTRACT_ADDRESS = _LidoAccountAddress;
emit LidoAccountChange(_LidoAccountAddress);

}


/**
track profits allowed to be sent to charities
 */

     function availableFundsForCharity() public  returns (uint256)  {

         uint256 totalBalance = IERC20(LIDO_FINANCE_CONTRACT_ADDRESS).balanceOf(address(this));

        require(totalBalance >= WPSharedPoolstkEthBalance,"WPFinance: Funds withdrawn");

        return totalBalance.sub(WPSharedPoolstkEthBalance);

     }


    

  /**
  stack whole ammount to lido finance
   */

  function lidoStakeEther(uint256 _amount) internal  {
  

     (bool sucess,) = LIDO_FINANCE_CONTRACT_ADDRESS.call{value : _amount}("");

    require(sucess,"WPFinance: Error Sending Eth to Lido");

    WPSharedPoolstkEthBalance = WPSharedPoolstkEthBalance.add(_amount);

    emit EthStakedToLido(_amount);

    }


/**

withdraw for future
 */
function withdrawAllFundsAndPause(address payable to)  public  whenNotPaused() onlyRole(DAO_ROLE)   {

uint256 balance = IERC20(LIDO_FINANCE_CONTRACT_ADDRESS).balanceOf(address(this));
IERC20 Lido = IERC20(LIDO_FINANCE_CONTRACT_ADDRESS);
Lido.transfer(to,balance);
WPSharedPoolstkEthBalance = 0;
emit FundsWithdrawn(to,balance);
_pause();


}

/**

withdraw rewards for charity by DAO
 */

 function withdrawForCharity(uint256 amount, address payable charity) public  onlyRole(DAO_ROLE)  {  
    require(amount <= availableFundsForCharity(),"WPFinance: amount greater than rewards");
     IERC20 Lido = IERC20(LIDO_FINANCE_CONTRACT_ADDRESS);
     Lido.transfer(charity, amount);
     
     emit FundsWithdrawnToCharity(charity, amount);
 }



}

