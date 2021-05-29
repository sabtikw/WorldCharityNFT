// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;




contract LidoDemo {
    
    mapping (address => uint256) internal balances;

 

    uint256 internal _totalSupply;

    string private _name;
    string private _symbol;

    constructor (string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
       
    }

event ethPrice(address indexed from); 

    receive() external payable {
        
emit ethPrice(msg.sender);
       balances[msg.sender] += msg.value;
           _totalSupply += msg.value;

    }
    
    function name() public view virtual  returns (string memory) {
        return _name;
    }

/**
@dev mimicks rebase functionality of LidoFinance

 */
function rebase(address WorldPeace) public {
    balances[WorldPeace]+= 1 ether;


}
   
    function symbol() public view virtual  returns (string memory) {
        return _symbol;
    }


    function decimals() public view virtual  returns (uint8) {
        return 18;
    }

   
    function totalSupply() public view virtual  returns (uint256) {
        return _totalSupply;
    }

    
    function balanceOf(address account) public view virtual  returns (uint256) {
        return balances[account];
    }

    function transfer(address recipient, uint256 amount) public virtual  returns (bool) {
         require(msg.sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");

       

        uint256 senderBalance = balances[msg.sender];
        require(senderBalance >= amount, "ERC20: transfer amount exceeds balance");
        unchecked {
            balances[msg.sender] = senderBalance - amount;
        }
        balances[recipient] += amount;

       
        return true;
    }

   

}