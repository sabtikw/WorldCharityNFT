import pytest
import brownie


WP_TOKEN_COUNT = 0
WP_TOKEN_PRICE = 0
tokenHash = [f"QmaozNR7DZHQK1ZcU9p7QdrshMvXqW{i}".encode() for i in range(10)]


@pytest.fixture(scope="module", autouse=True)
def worldPeace(WorldPeace,accounts):

    LidoERC20 = brownie.LidoDemo.deploy("Lido stkEth Demo","stkETH",{'from': accounts[0].address})
    wp = WorldPeace.deploy("World Peace Charity", "WPC", tokenHash,LidoERC20,accounts[0],{'from': accounts[0].address})
    global WP_TOKEN_COUNT
    global WP_TOKEN_PRICE
    WP_TOKEN_COUNT = wp.WP_TOKEN_COUNT()
    WP_TOKEN_PRICE = wp.WP_TOKEN_PRICE()

    yield wp


def test_mint_one_for_each_account(worldPeace,accounts):

    for i in range(WP_TOKEN_COUNT):
        worldPeace.mint({'from': accounts[i], 'value': WP_TOKEN_PRICE})

def test_tokenURIs(worldPeace):

    for hash, i in zip(tokenHash,range(WP_TOKEN_COUNT)):
            assert hash.decode() in worldPeace.tokenURI(i) 


def test_transfer_from_owner_without_eth_reverts(worldPeace, accounts):

    with brownie.reverts("World Peace: insufficient funds"):
     worldPeace.safeTransferFrom(accounts[0], accounts[1],0, {'from': accounts[0]})


def test_transfer_from_owner_with_eth(worldPeace, accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    ownerBalanceBefore = accounts[0].balance()
    contractBalance = Lido.balanceOf(worldPeace)
    value = 3e18

    worldPeace.safeTransferFrom(accounts[0], accounts[1],0, {'from': accounts[0], 'value': value})

    assert worldPeace.ownerOf(0) == accounts[1]
    assert worldPeace.balanceOf(accounts[0]) == 0
    assert worldPeace.balanceOf(accounts[1]) == 2
    assert accounts[0].balance() == ownerBalanceBefore - value*5/100
    assert Lido.balanceOf(worldPeace) == contractBalance + value*5/100


def test_transfer_from_non_owner_reverts(worldPeace, accounts):

    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        worldPeace.safeTransferFrom(accounts[1],accounts[0],3,{'from': accounts[1]})

def test_approve_from_owner(worldPeace, accounts):

    worldPeace.approve(accounts[0],0, {'from': accounts[1]})
    assert worldPeace.getApproved(0) == accounts[0]

def test_approve_from_non_owner_reverts(worldPeace, accounts):
    
    with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
        worldPeace.approve(accounts[2],0, {'from': accounts[3]})
    

def test_transfer_after_approval_without_eth_reverts(worldPeace, accounts):

    with brownie.reverts("World Peace: insufficient funds"):
     worldPeace.safeTransferFrom(accounts[1], accounts[0],0, {'from': accounts[0]})


def test_transfer_after_approval_with_eth(worldPeace, accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())

    balanceOfOwnerBefore = accounts[1].balance()
    contractBalance = Lido.balanceOf(worldPeace)
    value = 3e18

    worldPeace.safeTransferFrom(accounts[1], accounts[0],0, {'from': accounts[0], 'value': value})

    assert worldPeace.ownerOf(0) == accounts[0]
    assert worldPeace.balanceOf(accounts[0]) == 1
    assert accounts[1].balance() == balanceOfOwnerBefore + value  - value*5/100
    assert Lido.balanceOf(worldPeace) == contractBalance + value*5/100
    


def test_set_approve_for_all(worldPeace, accounts):

    worldPeace.setApprovalForAll(accounts[3], True,{'from': accounts[0]})

    assert worldPeace.isApprovedForAll(accounts[0],accounts[3])



def test_transfer_from_operator_with_eth(worldPeace, accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    balanceOfOwnerBefore = accounts[0].balance()
    contractBalance = Lido.balanceOf(worldPeace)
    value = 3e18

    worldPeace.safeTransferFrom(accounts[0], accounts[4],0, {'from': accounts[3], 'value': value})
    
    assert worldPeace.ownerOf(0) == accounts[4]
    assert worldPeace.balanceOf(accounts[4]) == 2
    assert accounts[0].balance() == balanceOfOwnerBefore + value  - value*5/100
    assert Lido.balanceOf(worldPeace) == contractBalance + value*5/100
