from django.shortcuts import render, redirect
import json
from web3 import Web3
from .forms import SetTime, TicketInfo

# web3.py instance
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/2ab636a3edbb446485e12966f841cea3"))

privateKey = "72FC57B03E230A54859AB16B69A62810786C8A388ABA43CA6FD96B258BA1A78A"
acct = w3.eth.account.privateKeyToAccount(privateKey)

# read the contract address and the abi from the json file
with open("ethereum/build/Railways.json", 'r') as f:
    factory_datastore = json.load(f)
abi = factory_datastore["abi"]
contract_address = factory_datastore["contract_address"]

# Create the contract instance with the newly-deployed address
rail = w3.eth.contract(
    address=contract_address, abi=abi
)

# Create your views here.
def settime(request):
    if request.method == 'POST':
        form = SetTime(request.POST)
        if form.is_valid():
            hh = int(form.cleaned_data.get('hh'))
            mm = int(form.cleaned_data.get('mm'))

            try:
                construct_txn = rail.functions.setTrain(hh, mm).buildTransaction({
                    'from': acct.address,
                    'nonce': w3.eth.getTransactionCount(acct.address)
                })
                # sign the transaction
                signed = acct.signTransaction(construct_txn)
                # get transaction hash
                tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                # Wait for transaction to be mined...
                w3.eth.waitForTransactionReceipt(tx_hash)
                return redirect('settime')
            except ValueError as e:
                return redirect('setime')
        else:
            return render(request, 'admin.html')
    else:
        return render(request, 'admin.html')


def depart(request):
    try:
        construct_txn = rail.functions.departure().buildTransaction({
            'from': acct.address,
            'nonce': w3.eth.getTransactionCount(acct.address)
        })
        signed = acct.signTransaction(construct_txn)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
        return render(request, 'admin.html')
    except ValueError as e:
        return render(request, 'trainregistration.html')


def ticketinfo(request):
    if request.method == 'POST':
        form = TicketInfo(request.POST)
        if form.is_valid():
            ticket_number = int(form.cleaned_data.get('ticket_number'))
            ticket = rail.functions.ticket_info(ticket_number).call()
            ticket[1] = Web3.fromWei(ticket[1], 'ether')
            ticket.pop()
            return render(request, 'ticket_information.html', {'data': ticket})
        else:
            return render(request, 'admin.html')
    else:
        return render(request, 'admin.html')
