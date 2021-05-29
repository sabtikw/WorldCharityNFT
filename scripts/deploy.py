
from  brownie import WorldPeace, LidoDemo, accounts

tokenHash = [f"QmaozNR7DZHQK1ZcU9p7QdrshMvXqW{i}".encode() for i in range(10)]


def main():

    LidoERC20 = LidoDemo.deploy("Lido stkEth Demo","stkETH",{'from': accounts[0].address})
    WorldPeace.deploy("World Peace Charity", "WPC", tokenHash,LidoERC20,accounts[0],{'from': accounts[0].address})
    
   