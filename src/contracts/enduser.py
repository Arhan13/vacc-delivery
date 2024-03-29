import smartpy as sp

# contract for end user
class Storage(sp.Contract):
    def __init__(self):
        self.init(vaccineCount = 0)
        
    @sp.entry_point
    def reqVaccFromDistributer(self, params):
        c = sp.contract(sp.TIntOrNat, address = params.address, entry_point="endUserRequest").open_some()
        sp.transfer(arg=params.amtVaccine, amount=sp.tez(0), destination = c)
        
    @sp.entry_point
    def processRequest(self, params):
        self.data.vaccineCount += params.quantity
        
@sp.add_test(name="Storage Example")
def test():
    alice = sp.test_account("Alice")
    c1 = Storage()
    scenario = sp.test_scenario()
    scenario.h1("Storage")
    scenario += c1
    scenario += c1.processRequest(quantity=20)
    scenario += c1.reqVaccFromDistributer(address=alice.address, amtVaccine=20)