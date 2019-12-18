import pickle
from web3 import Web3
from solcx import compile_files, link_code


privateKey = "72FC57B03E230A54859AB16B69A62810786C8A388ABA43CA6FD96B258BA1A78A"
# web3.py instance
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/2ab636a3edbb446485e12966f841cea3"))

def separate_main_n_link(file_path, contracts):
    # separate out main file and link files
    # assuming first file is main file.
    main = {}
    link = {}
    
    all_keys = list(contracts.keys())
    for key in all_keys:
        if file_path[0] in key:
            main = contracts[key]
        else:
            link[key] = contracts[key]
    return main, link


def deploy_contract(contract_interface):
    # access the account via private key
    acct = w3.eth.account.privateKeyToAccount(privateKey)
    # Instantiate and deploy contract
    contract_ = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    # build transaction
    construct_txn = contract_.constructor().buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')
        })
    # sign the transaction
    signed = acct.signTransaction(construct_txn)
    # Get transaction hash from deployed contract
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Get tx receipt to get contract address
    pending = True
    while pending:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash.hex())
        if tx_receipt != None:
            pending = False

    return tx_receipt['contractAddress']

    


def deploy_n_transact(file_path, mappings=[]):
    # compile all files
    contracts = compile_files(file_path, import_remappings=mappings)
    link_add = {}
    contract_interface, links = separate_main_n_link(file_path, contracts)

    # print (contract_interface)
    
    # first deploy all link libraries
    # here link is refers to the second contarct "stringUtils.sol"
    for link in links:
        link_add[link] = deploy_contract(links[link])    
    
    # now link dependent library code to main contract binary 
    # https://solidity.readthedocs.io/en/v0.4.24/using-the-compiler.html?highlight=library

    if link_add:
        contract_interface['bin'] = link_code(contract_interface['bin'], link_add)    
    
    # return contract receipt and abi(application binary interface)
    return deploy_contract(contract_interface), contract_interface['abi']