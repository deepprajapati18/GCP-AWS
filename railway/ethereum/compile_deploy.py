from c_solidity_utils import deploy_n_transact
import json

# Solidity source code
contract_address, abi = deploy_n_transact(['./contracts/Railways.sol'])


with open('./build/Railways.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)
