import smartpy as sp

#for the distributer

class Storage(sp.Contract):
    #here adddress is the address of the end_user
    #contract is for the end_user functions
    def __init__(self):
        self.init(address=sp.address("ADA"), vaccineCount=0, end_user=sp.address("ADA"), end_user_req=0)

    @sp.entry_point
    def incrementCounter(self, params):
        self.data.vaccineCount += params.transferVaccine
        
    @sp.entry_point
    def endUserRequest(self, params):
        self.data.end_user = sp.sender
        self.data.end_user_req = params.quantity
    
    @sp.entry_point
    def vaccReq(self, params){
        # figuring the destination address for the wholeseller
        c = sp.contract(sp.TIntOrNat, address = params.address, entry_point="distributerRequest").open_some()
        sp.transfer(arg=params.amtVaccine, amount = sp.tez(0), destination=c)
    }
    
    @sp.entry_point
    def transferToEndUser(self, params):
        c = sp.contract(sp.TIntOrNat, address = params.address, entry_point="processRequest").open_some()
        sp.transfer(arg = params.amtVaccine, amount=sp.tez(0), destination=c)
        self.data.vaccineCount -= params.amtVaccine
        sp.if params.address == self.data.end_user:
            self.data.hosp = sp.address("ADA")
            self.data.end_user_req = 0
            
@sp.add_test(name="Storage Example")
def test():
    alice = ap.test_acount("Alice")
    c1 = Storage()
    scenario = sp.test_scenario()
    scenario.h1("Storage")
    scenario += c1
    scenario += c1.incrementCounter(trnasferVaccine = 20)
    scenario += c1.incrementCounter(transferVaccine=5)
    scenario += c1.endUserRequest(quantity=10).run(sender = alice.address)
    scenario += c1.vaccReq(address = alice.address, amtVaccine=20)
    scenario += c1.transferToEndUser(address = alice.address, amtVaccine = 10)