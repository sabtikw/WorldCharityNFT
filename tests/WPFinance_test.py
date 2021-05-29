import pytest
import brownie

WP_TOKEN_COUNT = 0
WP_TOKEN_PRICE = 0
tokenHash = [f"QmaozNR7DZHQK1ZcU9p7QdrshMvXqW{i}".encode() for i in range(10)]

@pytest.fixture(scope="module", autouse=True)
def worldPeace(WorldPeace,accounts):

    Lido = brownie.LidoDemo.deploy("Lido stkEth Demo","stkETH",{'from': accounts[0].address})

    wp = WorldPeace.deploy("World Peace Charity", "WPC", tokenHash,Lido,accounts[0],{'from': accounts[0].address})

    global WP_TOKEN_COUNT
    global WP_TOKEN_PRICE
    WP_TOKEN_COUNT = wp.WP_TOKEN_COUNT()
    WP_TOKEN_PRICE = wp.WP_TOKEN_PRICE()

    for i in range(WP_TOKEN_COUNT):
        wp.mint({'from': accounts[i], 'value': WP_TOKEN_PRICE})

    
    yield wp


def test_sharedPool_balance_after_minting_all_tokens(worldPeace,accounts):

    assert worldPeace.WPSharedPoolstkEthBalance() == WP_TOKEN_PRICE * 10 - (WP_TOKEN_PRICE * 10 * 5 / 100)


def test_available_funds_before_rebase(worldPeace,accounts):

    assert worldPeace.availableFundsForCharity().return_value == 0
    
def test_available_funds_after_rebase(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    Lido.rebase(worldPeace)

    assert worldPeace.availableFundsForCharity().return_value == 1e18


def test_access_control_admin_check(worldPeace,accounts):

    assert worldPeace.hasRole(brownie.web3.keccak(text="ADMIN_ROLE"), accounts[0])


def test_access_control_operation_check(worldPeace,accounts):

    assert worldPeace.hasRole(brownie.web3.keccak(text="OPERATION_ROLE"),accounts[0])


def test_assign_DAO_role(worldPeace,accounts):

    worldPeace.grantRole(brownie.web3.keccak(text="DAO_ROLE"),accounts[9])

    assert worldPeace.hasRole(brownie.web3.keccak(text="DAO_ROLE"),accounts[9])


def test_withdraw_to_charity_more_than_available_reverts(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    Lido.rebase(worldPeace)

    assert worldPeace.availableFundsForCharity().return_value == 2e18

    with brownie.reverts("WPFinance: amount greater than rewards"):
        worldPeace.withdrawForCharity(5e18, accounts[8], {'from': accounts[9]})
    


def test_withdraw_to_charity_non_DAO_role(worldPeace,accounts):

    with brownie.reverts():
        worldPeace.withdrawForCharity(2e18, accounts[8], {'from': accounts[3]})


def test_withdraw_to_charity_half_amount(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    
    Lido.rebase(worldPeace)

    assert worldPeace.availableFundsForCharity().return_value == 3e18
    
    worldPeace.withdrawForCharity(3e18/2, accounts[7],{'from': accounts[9]})

    assert worldPeace.availableFundsForCharity().return_value == 3e18/2
    assert Lido.balanceOf(accounts[7]) == 3e18/2


def test_emergency_withdraw_all_fund_and_pause(worldPeace,accounts):

    Lido = brownie.LidoDemo.at(worldPeace.LIDO_FINANCE_CONTRACT_ADDRESS())
    contractBalance = Lido.balanceOf(worldPeace)

    assert worldPeace.hasRole(brownie.web3.keccak(text="DAO_ROLE"),accounts[9])

    worldPeace.withdrawAllFundsAndPause(accounts[5], {'from': accounts[9]})

    assert Lido.balanceOf(worldPeace) == 0
    assert Lido.balanceOf(accounts[5]) == contractBalance

def test_emergency_withdraw_after_pause(worldPeace,accounts):

    with brownie.reverts("Pausable: paused"):

        worldPeace.withdrawAllFundsAndPause(accounts[5], {'from': accounts[9]})

  