//SPDX-License-Identifier: MIT

pragma solidity 0.8.4;


import './ERC721.sol';
import '../interfaces/library/SafeMath.sol';
import './WPFinance.sol';



contract WorldPeace is ERC721, WPFinance {
        using SafeMath for uint256;


    
    bytes32[] tokensHash;
    uint256 public mintedWPTokens = 0;
    uint256 constant public WP_TOKEN_COUNT = 10;
    uint256 constant public WP_TOKEN_PRICE = 2 ether;
    
    

    constructor (string memory name__, string memory symbol__, bytes32[] memory tokensHash__, address payable LIDO_CONTRACT__, address payable WP_CREATOR__) ERC721(name__, symbol__) WPFinance(LIDO_CONTRACT__,WP_CREATOR__) {
        
       
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(OPERATION_ROLE,msg.sender);

        _setRoleAdmin(OPERATION_ROLE, ADMIN_ROLE);
        _setRoleAdmin(DAO_ROLE, ADMIN_ROLE);
       

        for (uint i = 0 ; i < WP_TOKEN_COUNT ; i++ ) {

            tokensHash.push(tokensHash__[i]); 
        }
    }



    /**
    add default recieve function to stak any excess recieved ether.
    */
    receive() external payable nonReentrant() {
  
  
        WPFinance.lidoStakeEther(msg.value);

  }

    fallback() external  {

    revert("World Peace: not implemented");

    }

function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721, AccessControl) returns (bool) {
        return interfaceId == type(IERC721).interfaceId
            || interfaceId == type(IERC721Metadata).interfaceId
            || interfaceId == type(AccessControl).interfaceId
            || interfaceId == type(IERC165).interfaceId;
            
            
    }

    
    function mint() external payable  {

    require(msg.value >= WP_TOKEN_PRICE, "WorldPeace: insufficient ether");
    require(mintedWPTokens < WP_TOKEN_COUNT, "WorldPeace: Tokens are sold out!");

    

    _safeMint(msg.sender,mintedWPTokens);
    
    mintedWPTokens = mintedWPTokens + 1;
    
    uint creatorEth = msg.value.mul(5).div(100);

    payable(CREATOR_ADDRESS).transfer(creatorEth);

    WPFinance.lidoStakeEther(msg.value.sub(creatorEth));

    

    }
  
 

    function transferFrom(address from, address to, uint256 tokenId) public  payable override {
        //solhint-disable-next-line max-line-length
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: transfer caller is not owner nor approved");
        require(msg.value > 0,"World Peace: insufficient funds"); // value has to be set by the owner with the approve and track it with the approve !
        _transfer(from, to, tokenId);
    }

  
    function safeTransferFrom(address from, address to, uint256 tokenId) public payable override {
        safeTransferFrom(from, to, tokenId, "");
    }

   
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public payable override {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: transfer caller is not owner nor approved");
        require(msg.value > 0,"World Peace: insufficient funds"); // value has to be set by the owner with the approve and track it with the approve !
        _safeTransfer(from, to, tokenId, _data);
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override nonReentrant() { 

        
        if (from != address(0)) {
        
        uint256 deduct = msg.value.mul(5).div(100);
        
        WPFinance.lidoStakeEther(deduct);  
       
        payable(ERC721.ownerOf(tokenId)).transfer(msg.value.sub(deduct));  

       
        
            }
      


}
   
    function _baseURI() internal pure override returns (string memory) {
        return "";
    }


     function tokenURI(uint256 tokenId) public view  override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0
            ? string(abi.encodePacked(baseURI, tokensHash[tokenId]))
            : '';
    }


}