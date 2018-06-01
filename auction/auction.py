def find_winner(bids):
    if len(bids) == 0:
        successful = False
        reason = "No bids were placed."
    else:
        best_bid = max([bids[x] for x in bids])
        winners = [x for x in bids if bids[x] == best_bid]
        if len(winners) == 1:
            successful = True
            reason = "The winner is **" + str(winners[0])[:-5] + "**, with a bid of " + str(best_bid) + "!"
        else:
            successful = False
            reason = "There was a tie.\n**" + str(winners[0])[:-5]
            for i in winners[1:]:
                reason += "**, **" + str(i)[:-5]
            reason += "** each bet *" + str(best_bid) + "*!"
    if successful:
        return [reason, winners[0], best_bid]
    else:
        return ["Auction failed: " + reason, 0]


def redist(wagers, extra):
    wagers = [x for x in wagers if x[1] != 0]
    if len(wagers) == 1:
        return [[], extra + wagers[0][1]]
    else:
        best = max([x[1] for x in wagers])
        to_distribute = extra + best
        total = sum([x[1] for x in wagers]) - best
        remnants = 0
        for x in wagers:
            if x[1] == best:
                x[1] = 0
            else:
                x[1] *= to_distribute
                x[1] /= total
                remnants += x[1] - int(x[1])
                x[1] = int(x[1])
        return [wagers, int(remnants)]
