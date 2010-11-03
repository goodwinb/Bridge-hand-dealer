import random
import itertools
from operator import itemgetter, attrgetter

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["c", "d", "h", "s"]


class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep


class Deck(object):

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + " "
        else:
            rep = "<empty>"
        return rep

    def add(self, card):
        self.cards.append(card)

    def deal(self, card, hand):
        try:
            hand.add(card)
            self.cards.remove(card)
        except Exception, f:
            msg = "Deck.deal error: " + str(f)
            print msg

    def get_length(self):
        length = len(self.cards)
        return length

    def get_card(self, index):
        your_card = self.cards[index]
        return your_card


class Hand(object):

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + " "
        else:
            rep = "<empty>"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

    def sort(self):
        sorted_hand = sorted(self.cards, key=lambda card: card.suit)
        rep = ""
        for card in sorted_hand:
            rep += str(card) + " "
        return rep

    def sortB(self):
        sorted_hand = sorted(self.cards, key=attrgetter('suit', 'rank'),
                             reverse=True)
        rep = ""
        for card in sorted_hand:
            rep += str(card) + " "
        return rep

    def spades(self):
        rep = ""
        spades = []
        for card in self.cards:
            if (card.suit == "s"):
                spades.append(card)
        spades_sorted = sorted(spades, key=attrgetter('rank'), reverse=True)
        return spades_sorted

    def hearts(self):
        rep = ""
        hearts = []
        for card in self.cards:
            if (card.suit == "h"):
                hearts.append(card)
        hearts_sorted = sorted(hearts, key=attrgetter('rank'), reverse=True)
        return hearts_sorted

    def diamonds(self):
        rep = ""
        diamonds = []
        for card in self.cards:
            if (card.suit == "d"):
                diamonds.append(card)
        diamonds_sorted = sorted(diamonds, key=attrgetter('rank'),
                                 reverse=True)
        return diamonds_sorted

    def clubs(self):
        rep = ""
        clubs = []
        for card in self.cards:
            if (card.suit == "c"):
                clubs.append(card)
        clubs_sorted = sorted(clubs, key=attrgetter('rank'), reverse=True)
        return clubs_sorted

    def count_points(self):
        points = 0
        for card in self.cards:
            if (card.rank == "A"):
                points = points + 4
            if (card.rank == "K"):
                points = points + 3
            if (card.rank == "Q"):
                points = points + 2
            if (card.rank == "J"):
                points = points + 1
        return points


def print_cards(cards):
    ss = ""
    for s in cards:
        ss += str(s) + " "
    return ss


# Deal four bridge hands and do a simple analysis
while True:
    reply = raw_input('Deal? (yes or no): ')
    if reply == 'yes':
        # Build a deck of cards
        deck = Deck()
        for rank in RANKS:
            for suit in SUITS:
                try:
                    my_card = Card(rank=rank, suit=suit)
                    deck.add(my_card)
                except Exception, e:
                    msg = str(e)
                    print msg

        # Deal out the hands and count points in the hands.
        card_count = deck.get_length()
        north = Hand()
        east = Hand()
        south = Hand()
        west = Hand()
        i = 0
        while (card_count > 39):
            r = random.randint(1, card_count) - 1
            random_card = deck.get_card(r)
            deck.deal(random_card, north)
            card_count = card_count - 1
        while (card_count > 26):
            r = random.randint(1, card_count) - 1
            random_card = deck.get_card(r)
            deck.deal(random_card, east)
            card_count = card_count - 1
        while (card_count > 13):
            r = random.randint(1, card_count) - 1
            random_card = deck.get_card(r)
            deck.deal(random_card, south)
            card_count = card_count - 1
        while (card_count > 0):
            r = random.randint(1, card_count) - 1
            random_card = deck.get_card(r)
            deck.deal(random_card, west)
            card_count = card_count - 1
        points_north = north.count_points()
        points_east = east.count_points()
        points_south = south.count_points()
        points_west = west.count_points()

        # Analyze the hands
        points_ns = points_north + points_south
        points_ew = points_east + points_west
        ns = False
        if (points_ns > points_ew):
            ns = True
        if ns:
            spade_count = len(north.spades()) + len(south.spades())
            hearts_count = len(north.hearts()) + len(south.hearts())
            diamonds_count = len(north.diamonds()) + len(south.diamonds())
            clubs_count = len(north.clubs()) + len(south.clubs())
            preferred_pair = 'North - South'
            counts = [('spades', spade_count), ('hearts', hearts_count),
                      ('diamonds', diamonds_count), ('clubs', clubs_count)]
            sorted_counts = sorted(counts, key=itemgetter(1), reverse=True)
            best_suit = sorted_counts[0]
            pair_points = str(points_ns)
        else:
            spade_count = len(east.spades()) + len(west.spades())
            hearts_count = len(east.hearts()) + len(west.hearts())
            diamonds_count = len(east.diamonds()) + len(west.diamonds())
            clubs_count = len(east.clubs()) + len(west.clubs())
            preferred_pair = 'East - West'
            counts = [('spades', spade_count), ('hearts', hearts_count),
                      ('diamonds', diamonds_count), ('clubs', clubs_count)]
            sorted_counts = sorted(counts, key=itemgetter(1), reverse=True)
            best_suit = sorted_counts[0]
            pair_points = str(points_ew)
        print '\t\t\tNorth:'
        print '\t\t\tpoints: ' + str(points_north)
        print '\t\t\tS: ' + (print_cards(north.spades()))
        print '\t\t\tH: ' + (print_cards(north.hearts()))
        print '\t\t\tD: ' + (print_cards(north.diamonds()))
        print '\t\t\tC: ' + (print_cards(north.clubs())) + '\n'
        print 'West: ', ' '.ljust(37), 'East: '
        print 'points: ' + str(points_west), ' '.ljust(34),
        'points: ' + str(points_east)
        print 'S: ', print_cards(west.spades()).ljust(40),
        'S: '.rjust(3), print_cards(east.spades()).ljust(18)
        print 'H: ', print_cards(west.hearts()).ljust(40),
        'H: '.rjust(3), print_cards(east.hearts()).ljust(18)
        print 'D: ', print_cards(west.diamonds()).ljust(40),
        'D: '.rjust(3), print_cards(east.diamonds()).ljust(18)
        print 'C: ', print_cards(west.clubs()).ljust(40),
        'C: '.rjust(3), print_cards(east.clubs()).ljust(18)
        print '\t\t\tSouth:'
        print '\t\t\tpoints: ' + str(points_south)
        print '\t\t\tS: ' + print_cards(south.spades())
        print '\t\t\tH: ' + print_cards(south.hearts())
        print '\t\t\tD: ' + print_cards(south.diamonds())
        print '\t\t\tC: ' + print_cards(south.clubs()) + '\n'
        print preferred_pair + ' should play. They have ' +
        pair_points + ' points.'
        print best_suit
        print '\n'
    else:
        break
print 'Bye'
