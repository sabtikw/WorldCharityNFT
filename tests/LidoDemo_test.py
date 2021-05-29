import pytest
import brownie


@pytest.fixture
def Lidodemo(LidoDemo,accounts):
    return LidoDemo.deploy("Lido stkEth Demo","stkETH",{'from': accounts[0].address})
    


def test_send_eth_and_receive_stkEth(Lidodemo,accounts):

    assert Lidodemo.balanceOf(accounts[1]) == 0

    accounts[1].transfer(Lidodemo.address,'11 ether')

    assert  Lidodemo.balanceOf(accounts[1]) == 11e18
    assert Lidodemo.balanceOf(accounts[2]) == 0

    accounts[2].transfer(Lidodemo.address,'11 ether')

    assert  Lidodemo.balanceOf(accounts[2]) == 11e18

def test_transfer_stkEth(Lidodemo,accounts):

    accounts[1].transfer(Lidodemo.address,'11 ether')

    Lidodemo.transfer(accounts[0],2e18,{'from': accounts[1]})
    
    assert Lidodemo.balanceOf(accounts[0]) == 2e18

