import smartpy as sp

class Storage(sp.Contract):
    def __init__(self):
        self.init(address=sp.address("DIS"), vaccineAvailable=0, req=0)
    
    @sp.entry_point
    def updateVacc(self, params):
        self.data.vaccineAvailable = params.vaccCount

    @sp.entry_point
    def distributerReq(self, params):
        self.data.address = sp.sender
        self.data.req = params.quantity

    @sp.entry_point
    def transferVaccToDistributer(self, params):
        self.data.address = params.address
        c = sp.conract(sp.TInt, address=self.data.address, entry_point="incrementCounter").open_some()
        sp.transfer(arg=params.reqVaccine, amount=sp.tez(0), destination = c)
        self.data.vaccineAvailable -= params.reqAmount
        sp.if params.address==self.data.address:
            self.data.address = sp.address("DIS")
            self.data.req = 0

@sp.add_test(name="Storage Example")
def test():
    alice = sp.test_account("Alice")
    c1 = Storage()
    scenario  sp.test_scenario()
    scenario.h1("Storage")
    scenario += c1
    scenario += c1.updateVacc(vaccCount=100000)
    scenario += c1.distributerReq(quantity=200).run(sender = alice.address)
    scenario += c1.transferVaccToDistributer(address=alice.address, reqVaccine=200)