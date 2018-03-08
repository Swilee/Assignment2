import numpy as np
from enum import Enum
from enum import IntEnum


class Suit(Enum):
    """
    Here an enum class is created to represent the suits.
    """
    Hearts = 0
    Spades = 1
    Diamonds = 2
    Clubs = 3


class CardCombo(IntEnum):
    """
    Here an enum class is created to represent the different values of pokenhands.
    """
    highcard = 0
    onepair = 1
    twopair = 2
    threeofakind = 3
    straight = 4
    flush = 5
    fullhouse = 6
    fourofakind = 7
    straightflush = 8

Uni = [u'\u2665', u'\u2660', u'\u2666', u'\u2663']
#Hearts = u'\u2665'
#suit.Clubs = u'\u2663'
#suit.Spades = u'\u2660'
#suit.Diamonds = u'\u2666'


class PlayingCard:
    """
    Here a playingcard class is defined to be comparable.
    """

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value


class NumberedCard(PlayingCard):
    """
    In this class the playingcards without a suit are represented.
    """
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.uni = Uni[suit.value]
        self.symbol=str(value)


class JackCard(PlayingCard):
    def __init__(self, suit):
        self.suit = suit
        self.value = 11
        self.uni = Uni[suit.value]
        self.symbol = 'J'


class QueenCard(PlayingCard):
    def __init__(self, suit):
        self.suit = suit
        self.value = 12
        self.uni = Uni[suit.value]
        self.symbol = 'Q'


class KingCard(PlayingCard):
    def __init__(self, suit):
        self.suit = suit
        self.value = 13
        self.uni = Uni[suit.value]
        self.symbol = 'K'


class AceCard(PlayingCard):
    def __init__(self, suit):
        self.suit = suit
        self.value = 14
        self.uni = (Uni[suit.value])
        self.symbol = 'A'


class Deck:
    """
    The deck class can be used to create a deck of 52 cards, shuffle the deck and remove the top card of the deck.
    """

    def __init__(self):
        self.deck = np.array([])
        for j in range(0, 4):
            for i in range(2, 11):
                self.deck = np.append(self.deck, NumberedCard(i, Suit(j)))
            self.deck = np.append(self.deck, JackCard(Suit(j)))
            self.deck = np.append(self.deck, QueenCard(Suit(j)))
            self.deck = np.append(self.deck, KingCard(Suit(j)))
            self.deck = np.append(self.deck, AceCard(Suit(j)))


    def ShuffleDeck(self, deck):
        np.random.shuffle(deck)
        return deck

    def TakeTopCard(self, deck):
        topcard = deck[-1]
        deck = np.delete(deck, -1)

        return deck, topcard


class PlayerHand():
    """
    The playerhand class can be used to create a player hand. The hand may be given cards, have cards removed,
    sorted and evaluated for the best poker hand.
    """
    def __init__(self):
        self.cards = np.array([])
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def givecard(self, card):
        self.cards = np.append(self.cards, card)
        return self.cards

    def removecard(self, index):
        self.cards = np.delete(self.cards, index)
        return self.cards

    def sortcards(self):
        return np.sort(self.cards)

    def best_poker_hand(self, cards=[]):
        cards = np.append(self.cards, cards)
        value_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        suit_count = [0, 0, 0, 0]
        for card in cards:
            val = card.value
            value_count[val-2] += 1
            suit = card.suit
            suit_count[suit.value] += 1

        v = self.check_straight_flush(value_count, suit_count)
        if v is not None:
            return v

        v = self.check_four_of_a_kind(value_count)
        if v is not None:
            return v

        v = self.check_full_house(value_count)
        if v is not None:
            return v

        v = self.check_flush(suit_count)
        if v is not None:
            return v

        v = self.check_straight(value_count)
        if v is not None:
            return v

        v = self.check_three_of_a_kind(value_count)
        if v is not None:
            return v

        v = self.check_two_pair(value_count)
        if v is not None:
            return v

        v = self.check_one_pair(value_count)
        if v is not None:
            return v
        else:
            v = CardCombo.highcard
            return v

    @staticmethod
    def check_one_pair(value_count):
        if 2 in value_count:
            return CardCombo.onepair

    @staticmethod
    def check_two_pair(value_count):
        if value_count.count(2) >= 2:
            return CardCombo.twopair


    @staticmethod
    def check_three_of_a_kind(value_count):
        if 3 in value_count:
            return CardCombo.threeofakind

    @staticmethod
    def check_straight(value_count):
        n = 0
        for i in value_count:
            if n == 10:
                return
            else:
                pass
            if i != 0:
                if value_count[n + 1] != 0:
                    if value_count[n + 2] != 0:
                        if value_count[n + 3] != 0:
                            if value_count[n + 4] != 0:
                                return CardCombo.straight
            else:
                pass
            n = n + 1

    @staticmethod
    def check_flush(suit_count):
        if 5 in suit_count:
            return CardCombo.flush

    @staticmethod
    def check_full_house(value_count):
        if 3 in value_count:
            if 2 in value_count:
                return CardCombo.fullhouse

    @staticmethod
    def check_four_of_a_kind(value_count):
        if 4 in value_count:
            return CardCombo.fourofakind
    @staticmethod
    def check_straight_flush(value_count, suit_count):
        if 5 in suit_count:
            n = 0
            for i in value_count:
                if n == 10:
                    return
                else:
                    pass
                if i != 0:
                    if value_count[n + 1] != 0:
                        if value_count[n + 2] != 0:
                            if value_count[n + 3] != 0:
                                if value_count[n + 4] != 0:
                                    return CardCombo.straightflush
                else:
                    pass
                n = n + 1

