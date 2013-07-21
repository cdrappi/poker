import random
import math
import itertools

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key = hand_rank)

def allmax(iterable, key = lambda x:x):
    "Return a list of all items equal to the max of the iterable."
    maxval = None
    maxitems = []
    for item in iterable:
        keyval = key(item)
        if maxval is None or keyval > maxval:
            maxval = keyval
            maxitems = [item]
        elif keyval == maxval:
            maxitems.append(item)
    return maxitems

def hand_rank(hand):
    "Return a value indicating how high the hand ranks."
    # counts is the count of each rank
    # ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return (
        9 if (5, ) == counts else
        8 if straight and flush else
        7 if (4, 1) == counts else
        6 if (3, 2) == counts else
        5 if flush else
        4 if straight else
        3 if (3, 1, 1) == counts else
        2 if (2, 2, 1) == counts else
        1 if (2, 1, 1, 1) == counts else
        0), ranks

def group(items):
    "Return a list of [(count, x)...], highest count first, the highest x first"
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse = True)

def unzip(pairs):
    return zip(*pairs)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    # ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    # ranks = [{'A':14,
    #           'K':13,
    #           'Q':12,
    #           'J':11,
    #           'T':10,
    #           }.get(r,r) for r, s in hand]
    ranks = [14 if r == 'A' else
             13 if r == 'K' else
             12 if r == 'Q' else
             11 if r == 'J' else
             10 if r == 'T' else
             int(r)
             for r, s in hand]
    ranks.sort(reverse = True)
    # ace high straights
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]
    return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return sum(ranks) - min(ranks)*5 == 10

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    result = [r for r in set(ranks) if ranks.count(r) == 2]
    if len(result) == 2:
        return (max(result), min(result))

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in set(ranks):
        if ranks.count(r) == n:
            return r
    return None

def deal(numhands, n = 5, deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Return a list of numhands hands consisting of n cards each"
    random.shuffle(deck)
    deck = iter(deck)
    return [[next(deck) for card in range(n)] for hand in range(numhands)]

hand_names = [
    'High Card',
    'Pair',
    '2 Pair',
    '3 Kind',
    'Straight',
    'Flush',
    'Full House',
    '4 Kind',
    'Straight Flush',
    ]

def hand_percentages(n = 700*1000):
    "Sample n random hands and print a table of percentages for each type of hand"
    counts = [0]*9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print('%14s: %6.3f'%(hand_names[i], 100.*counts[i]/n))

def all_hand_percentages():
    "Print an exhaustive table of frequencies for each type of hand"
    counts = [0]*9
    n = 0
    deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
    for hand in itertools.combinations(deck, 5):
        n += 1
        ranking = hand_rank(hand)[0]
        counts[ranking] += 1
    for i in reversed(range(9)):
        print('%14s: %7d %6.3f'%(hand_names[i], counts[i], 100.*counts[i]/n))

def shuffle1(deck):
    # O(N**2)
    # incorrect distribution
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle2(deck):
    # O(N**2)
    # incorrect distribution?
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle2a(deck):
    # http://forums.udacity.com/cs212-april2012/questions/3462/better-implementation-of-shuffle2
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        j = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle3(deck):
    # O(N)
    # incorrect distribution
    N = len(deck)
    for i in range(N):
        j = random.randrange(N)
        deck[i], deck[j] = deck[j], deck[i]

def knuth(deck):
    n = len(deck)
    for i in range(n-1):
        j = random.randrange(i, n)
        deck[i], deck[j] = deck[j], deck[i]

def holdem_deal(numhands, sim_hand = False, n = 2, community_cards = 5, deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Return a list of numhands hands consisting of n cards each"
    # if we want to hold out a hand
    hands_to_deal = numhands
    random.shuffle(deck)
    pockets = []
    if sim_hand:
        # remove hands we're simulating
        deck = list(set(deck) - set(sim_hand))
        hands_to_deal -= 1
        pockets.append(sim_hand)
    deck = iter(deck)
    pockets.extend([[next(deck) for card in range(n)] for hand in range(hands_to_deal)])
    community = [next(deck) for card in range(community_cards)]
    return pockets, community

def pocket_in_words(pocket):
    ret = ""
    ranks = card_ranks(pocket)
    ret = card_to_words(ranks[0]) + card_to_words(ranks[1])
    if pocket[0][1] == pocket[1][1]:
        ret += "s"
    # We do this to not give "o" to pairs.
    elif pocket[0][0] != pocket[1][0]:
        ret += "o"
    return ret

def list_to_str(l):
    return " ".join(l)

def str_to_list(s):
    return s.split()

def card_to_words(card):
    if card == "A" or card == 14:
        return "A"
    elif card == "K" or card == 13:
        return "K"
    elif card == "Q" or card == 12:
        return "Q"
    elif card == "J" or card == 11:
        return "J"
    elif card == "T" or card == 10:
        return "T"
    else:
        return str(card)

def tuple_to_str(t):
    return ' '.join(map(str,t))

def str_to_tuple(s):
    l = s.split()
    return tuple(l)