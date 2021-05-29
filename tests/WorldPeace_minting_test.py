import pytest
import brownie

# test fallack and receive!!!
# test events !
WP_TOKEN_COUNT = 0
WP_TOKEN_PRICE = 0
tokenHash = [f"QmaozNR7DZHQK1ZcU9p7QdrshMvXqW{i}".encode() for i in range(10)]


@pytest.fixture
def worldPeace(WorldPeace,accounts):
    LidoERC20 = brownie.LidoDemo.deploy("Lido stkEth Demo","stkETH",{'from': accounts[0].address})
    wp = WorldPeace.deploy("World Peace Charity", "WPC", tokenHash,LidoERC20, accounts[0], {'from': accounts[0].address})
    global WP_TOKEN_COUNT
    global WP_TOKEN_PRICE
    WP_TOKEN_COUNT = wp.WP_TOKEN_COUNT()
    WP_TOKEN_PRICE = wp.WP_TOKEN_PRICE()
    return wp



def test_worldpeace_name(worldPeace):
    "get benefeciary name"

    assert worldPeace.name() == "World Peace Charity", 'NFT name doesn\'t match the construcor name'


def test_worldpeace_symbol(worldPeace):
    "get benefeciary name"

    assert worldPeace.symbol() == "WPC", 'NFT Symbol doesn\'t match the construcor symbol'


def test_tokenURIs_reverts(worldPeace):

    with brownie.reverts("ERC721Metadata: URI query for nonexistent token"):
        for hash, i in zip(tokenHash,range(WP_TOKEN_COUNT)):
            assert   hash.decode() in worldPeace.tokenURI(i) 


def test_mint(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    contractBalance = Lido.balanceOf(worldPeace)

    worldPeace.mint({'from': accounts[1], 'value': WP_TOKEN_PRICE})

    assert  worldPeace.balanceOf(accounts[1].address) == 1
    assert  worldPeace.ownerOf(0) == accounts[1].address
    assert worldPeace.mintedWPTokens() == 1
    assert Lido.balanceOf(worldPeace) == contractBalance + (2e18 - (2e18*5/100))
    



def test_mint_without_ether_reverts(worldPeace,accounts):

    with brownie.reverts("WorldPeace: insufficient ether"):
        worldPeace.mint({'from': accounts[1]})


def test_mint_with_less_ether_reverts(worldPeace,accounts):

    with brownie.reverts("WorldPeace: insufficient ether"):
        worldPeace.mint({'from': accounts[1], 'value': WP_TOKEN_PRICE - 1e18})

def test_mint_with_extra_ether(worldPeace,accounts):

    value = WP_TOKEN_PRICE + 1e18

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    contractBalance = Lido.balanceOf(worldPeace)

    worldPeace.mint({'from': accounts[2], 'value': value})

    assert  worldPeace.balanceOf(accounts[2].address) == 1
    assert  worldPeace.ownerOf(0) == accounts[2].address
    assert Lido.balanceOf(worldPeace) == contractBalance + (value - (value*5/100))

def test_mint_for_multiple_accounts(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    contractBalance = Lido.balanceOf(worldPeace)
    for i in range(WP_TOKEN_COUNT):
       
        worldPeace.mint({'from': accounts[i], 'value': WP_TOKEN_PRICE})

        assert  worldPeace.balanceOf(accounts[i].address) == 1
        assert  worldPeace.ownerOf(i) == accounts[i].address

    assert worldPeace.mintedWPTokens() == WP_TOKEN_COUNT
    assert Lido.balanceOf(worldPeace) == contractBalance + (WP_TOKEN_PRICE * WP_TOKEN_COUNT - (WP_TOKEN_PRICE * 10 * 5 / 100))

def test_mint_two_tokens_for_one_account(worldPeace,accounts):

    worldPeace.mint({'from': accounts[2], 'value': WP_TOKEN_PRICE})
    worldPeace.mint({'from': accounts[2], 'value': WP_TOKEN_PRICE})

    assert  worldPeace.balanceOf(accounts[2].address) == 2
    assert  worldPeace.ownerOf(0) == accounts[2].address
    assert  worldPeace.ownerOf(1) == accounts[2].address

def test_mint_more_than_token_count_reverts(worldPeace,accounts):
    
    with brownie.reverts("WorldPeace: Tokens are sold out!"):
        for i in range(WP_TOKEN_COUNT + 1):
            worldPeace.mint({'from': accounts[1], 'value': 2e18})


    