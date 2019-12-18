from django.shortcuts import render, redirect
from .forms import TicketForm
import json
from web3 import Web3

# web3.py instance
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/2ab636a3edbb446485e12966f841cea3"))

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
def buyticket(request):
	if request.method == 'POST':
		form = TicketForm(request.POST)
		if form.is_valid():
			privateKey = form.cleaned_data.get('privateKey')
			ticket_number = int(form.cleaned_data.get('ticket_number'))
			price = int(form.cleaned_data.get('price'))

			acct = w3.eth.account.privateKeyToAccount(privateKey)
			try:
				construct_txn = rail.functions.buyTicket(ticket_number).buildTransaction(
					{
						'from': acct.address,
						'value': w3.toWei(price, 'ether'),
						'nonce': w3.eth.getTransactionCount(acct.address)
					})

				signed = acct.signTransaction(construct_txn)

				tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
				
				# Wait for transaction to be mined...
				w3.eth.waitForTransactionReceipt(tx_hash)
				return redirect('buyticket')

			except ValueError as e:
				msg = e.args[0]['message']
				messages.error(request, msg)
				return redirect('buyticket')
		else:
			return render(request, 'trainregistration.html')
	else:
		return render(request, 'trainregistration.html')


def refund_info(request):
	data = {}
	length = rail.functions.user_length().call()
	for i in range(int(length)):
		address = rail.functions.user(i).call()
		refund = rail.functions.returned_info(address).call()
		data[address] = Web3.fromWei(refund, 'ether')

	return render(request, 'refund.html', {'data': data})
