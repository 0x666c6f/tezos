import smartpy as sp

class SimpleLottery(sp.Contract):
    def __init__(self, owner, max_tickets):
        self.init(owner = owner, ticket_cost = 1000, total_tickets = 5, current_ticket = 0, lottery_registry = sp.map(tkey = sp.TNat, tvalue = sp.TAddress))

    @sp.entry_point
    def buy_ticket(self):
        sp.verify(sp.amount > sp.mutez(0), message = "Amount should be > 0")
        ticket_nb_ediv = sp.ediv(sp.amount, sp.mutez(self.data.ticket_cost))
        sp.verify(ticket_nb_ediv.is_some(), message = "Amount is incorrect, can't process number of tickets to buy")
        sp.verify(sp.snd(ticket_nb_ediv.open_some()) == sp.tez(0), message = "Amount is incorrect, total is not a direct multiplier of the ticket price")
        ticket_nb = sp.fst(ticket_nb_ediv.open_some())
        sp.verify(ticket_nb > 0,  message = "Amount is incorrect, total ticket number to buy must be > 0")
        sp.verify(ticket_nb <= self.data.total_tickets, message = "Amount is incorrect, total ticket number to buy must be < to total ticket number")
        sp.verify(self.data.current_ticket < self.data.total_tickets, message = "Error, can't sell more than the total ticket number")
        i = sp.local("i",0)
        sp.while i.value < ticket_nb:
            self.data.lottery_registry[self.data.current_ticket] = sp.sender
            self.data.current_ticket += 1
            i.value = (i.value + 1)
            sp.if self.data.current_ticket == self.data.total_tickets:
                self.select_winner()
                self.data.lottery_registry = sp.map()
                self.data.current_ticket = 0
                

    def select_winner(self):
        winner = sp.local("winner",sp.as_nat(sp.timestamp_from_utc_now() - sp.timestamp_from_utc(1970, 1, 1, 0, 0, 0)) % self.data.total_tickets)
        sp.send(self.data.lottery_registry[winner.value], sp.mutez(self.data.ticket_cost *5))

    @sp.entry_point
    def change_ticket_price(self, new_price):
        sp.verify(sp.sender == self.data.owner, message = "Error, only the owner can change the ticket price")
        sp.verify(sp.len(self.data.lottery_registry) == 0, message = "Error, can't change the ticket price when some tickets have already been sold")
        sp.verify(sp.mutez(new_price) < sp.tez(1), message = "Error, ticket price must be < to 1 XTZ")
        sp.verify(sp.mutez(new_price) > sp.mutez(0), message = "Error, ticket price must be > to 1 muXTZ")
        self.data.ticket_cost = new_price
        
    @sp.entry_point
    def change_ticket_total(self, new_total):
        sp.verify(sp.sender == self.data.owner, message = "Error, only the owner can change the ticket total")
        sp.verify(sp.len(self.data.lottery_registry) == 0, message = "Error, can't change the ticket total when some tickets have already been sold")
        sp.verify(new_total > 0, message = "Error, ticket total must be > to 0")
        sp.verify(new_total <= 10, message = "Error, ticket price must be < to 10")
        self.data.total_tickets = new_total
        
@sp.add_test(name = "Test SimpleLottery")
def test():
    scenario  = sp.test_scenario()

    scenario.h1("Simple Test Lottery")
    owner = sp.test_account("owner")
    player1     = sp.test_account("player1")
    player2     = sp.test_account("player2")
    player3     = sp.test_account("player3")
    player4     = sp.test_account("player4")
    player5     = sp.test_account("player5")

    lottery = SimpleLottery(owner.address, max_tickets = 5)
    scenario += lottery
    
    scenario.h2("Price change tests (before buying)")
    scenario.h3("Successful Price change tests (before buying)")
    scenario += lottery.change_ticket_price(2000).run(sender = owner)
    scenario += lottery.change_ticket_price(1000).run(sender = owner)
    scenario.h3("Failing Price change tests (before buying)")
    scenario += lottery.change_ticket_price(1000000000).run(sender = owner, valid = False)
    scenario += lottery.change_ticket_price(1000).run(sender = player1, valid = False)
    scenario += lottery.change_ticket_price(1000000000).run(sender = player1, valid = False)
    
    scenario.h2("Ticket total tests (before buying)")
    scenario.h3("Successful Ticket total tests (before buying)")
    scenario += lottery.change_ticket_total(5).run(sender = owner)
    scenario += lottery.change_ticket_total(10).run(sender = owner)
    scenario += lottery.change_ticket_total(5).run(sender = owner)
    scenario.h3("Failing Ticket total tests (before buying)")
    scenario += lottery.change_ticket_total(0).run(sender = owner, valid = False)
    scenario += lottery.change_ticket_total(11).run(sender = owner, valid = False)
    scenario += lottery.change_ticket_total(10).run(sender = player1, valid = False)
    scenario += lottery.change_ticket_total(5).run(sender = player1, valid = False)
    
    scenario.h2("Ticket buying tests")
    scenario += lottery.buy_ticket().run(sender= player1, amount = sp.mutez(1000))
    scenario += lottery.buy_ticket().run(sender= player2, amount = sp.mutez(1000))
    scenario += lottery.buy_ticket().run(sender= player3, amount = sp.mutez(1000))
    scenario += lottery.buy_ticket().run(sender= player4, amount = sp.mutez(1000))
    scenario += lottery.buy_ticket().run(sender= player5, amount = sp.mutez(1000))
    scenario.h1("Balances")
    scenario.show("Player1:")
    scenario.show(player1)
    scenario += lottery.buy_ticket().run(sender= player2, amount = sp.mutez(6000), valid = False)



