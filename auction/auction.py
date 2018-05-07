# I lost track of what I was doing partway through writing this, so I'm leaving it here for now

class Auction:
    def __init__(self, item_list):
        self.items = item_list
        self.members = {}
        self.wagers = {}
        for i in item_list:
            self.wagers[i] = {}
    def add_member(self, user):
        self.members[str(user), 100]
    def collect_wager(self, user, proposed_wager):
        wager = int(proposed_wager)
        if self.members[str(user)] < wager:
            wager = self.members[str(user)]

# Seriously though, I can't remember how this was supposed to work under the hood.



