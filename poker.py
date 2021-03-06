import numpy as np
from enum import Enum
from enum import IntEnum
from abc import ABC, abstractmethod


class Suit(Enum):
    """
    Here an enum class is created to represent the suits.
    """
    Hearts = 0
    Spades = 2
    Diamonds = 1
    Clubs = 3

    #def __str__(self):
    #    return [u'\u2665', u'\u2666', u'\u2660', u'\u2663'][self.value]



class HighCard(IntEnum):
    """
    The high card values are represented by an enum class.
    """
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14


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

class PlayingCard(ABC):
    """
    Here a playingcard class is defined to be comparable.
    """

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    @abstractmethod
    def give_value(self):
        pass

    def __str__(self):
        return '%s %s' %(self.symbol , self.uni)

    Uni = [u'\u2665', u'\u2666', u'\u2660', u'\u2663']


class NumberedCard(PlayingCard):
    """
    In this class the playingcards without a suit are represented.
    """
    def __init__(self, value, suit):
        super().__init__()
        self.value = value
        self.suit = suit
        self.uni = self.Uni[suit.value]
        self.symbol = str(value)

    def give_value(self):
        return self.value


class JackCard(PlayingCard):
    """
    The JackCard class represents the jack card
    """
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 11
        self.uni = self.Uni[suit.value]
        self.symbol = 'J'

    def give_value(self):
        return self.value


class QueenCard(PlayingCard):
    """
    The QueenCard class represents the queen card.
    """
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 12
        self.uni = self.Uni[suit.value]
        self.symbol = 'Q'

    def give_value(self):
        return self.value


class KingCard(PlayingCard):
    """
    The KingCard class represents the king card.
    """
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 13
        self.uni = self.Uni[suit.value]
        self.symbol = 'K'

    def give_value(self):
        return self.value


class AceCard(PlayingCard):
    """
    The AceCard class represents the ace card.
    """
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 14
        self.uni = self.Uni[suit.value]
        self.symbol = 'A'

    def give_value(self):
        return self.value


class Deck(object):
    """
    In the Deck class, 52 cards are created and stored in the "deck" variable.
    """
    def __init__(self):
        deck = np.array([])
        for j in range(0, 4):
            for i in range(2, 11):
                deck = np.append(deck, NumberedCard(i, Suit(j)))
            deck = np.append(deck, JackCard(Suit(j)))
            deck = np.append(deck, QueenCard(Suit(j)))
            deck = np.append(deck, KingCard(Suit(j)))
            deck = np.append(deck, AceCard(Suit(j)))
        self.deck = deck

    def shuffle_deck(self):
        '''Randomly shuffles the Deck objects deck'''
        np.random.shuffle(self.deck)

    def take_top_card(self):
        '''
        takes the top card from the deck
        :return: the deck itself without the topcard
                and the topcard itself
        '''
        topcard = self.deck[-1]
        self.deck = np.delete(self.deck, -1)

        return topcard


class PlayerHand:
    """
    The playerhand class can be used to create a player hand. The hand may be given cards, have cards removed,
    sorted and evaluated for the best poker hand.
    """

    def __init__(self):
        self.cards = np.array([])

    def give_card(self, card):
        '''
        Adds a card to the hand.
        :param card: The PlayingCard object to be added
        :return The cards, with the specified card added
        '''
        self.cards = np.append(self.cards, card)


    def remove_card(self, index):
        '''
        Removes the card in the hand at the specified indicies
        :param index: indices for card to be removed
        :return The cards, with the specified card removed
        '''
        self.cards = np.delete(self.cards, index)

    def sort_cards(self):
        '''Sorts the cards in the hand'''
        return np.sort(self.cards)


    def best_poker_hand(self, cards):
        '''
        Computes the best pokerhand out of a set of cards
        :param cards: a single PlayingCard or a list of PlayingCard objects
        :return a PokerHand object containing the CardCombo and the highest cards
        '''
        cards = np.append(self.cards, cards)
        value_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.card_combo = None

        suit_card_connector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        suit_count = [0, 0, 0, 0]
        for card in cards:
            val = card.value
            value_count[val-1] += 1
            suit = card.suit
            suit_count[suit.value] += 1
        if max(suit_count) >= 5:
            for card in cards:
                if card.suit.value == suit_count.index(max(suit_count)):
                    suit_card_connector[card.value - 1] = 1
        if sum(value_count) == 0:
            raise ValueError('No cards in hand or on table')

        v, card_values = self.check_straight_flush(suit_card_connector, suit_count)
        if card_values is not None:
            self.card_combo = v
            self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_four_of_a_kind(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_full_house(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_flush(suit_count, suit_card_connector)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_straight(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_three_of_a_kind(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v , card_values = self.check_two_pair(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_one_pair(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            self.card_combo, self.card_values = self.high_card(value_count)

        self.pokerhand = PokerHand(self.card_combo, self.card_values)

    @staticmethod
    def high_card(value_count):
        ''' Checks for the 5 highest cards in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  list of the 5 highest cards
        '''
        card_values = []
        for j, data in reversed(list(enumerate(value_count))):
            if data == 1:
                card_values.append(j + 1)
        return CardCombo.highcard, card_values[0:5]

    @staticmethod
    def check_one_pair(value_count):
        '''
        Checks for a pair in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no pair is found, else 1 ( value of a pair) and a list with the
        pair and the 3 highest cards exluding the pair
        '''
        if 2 in value_count:
            card_values = [value_count.index(2)+1]
            for j, data in reversed(list(enumerate(value_count))):
                if data == 1:
                    card_values.append(j+1)

            return 1, card_values[0:4]
        else:
            return None, None

    @staticmethod
    def check_two_pair(value_count):
        '''
        Checks for the highest two pair in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 2 ( the value of a two pair) and
        a list with the pairs and the highest card exluding the two pair
        '''
        if value_count.count(2) >= 2:
            #lägg till det största paret först i card_values samt ta bort det för att kunna ta det näst högsta paret
            pairs = []
            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 2:
                    pairs.append(j+1)
                elif data == 1:
                    single_cards.append(j+1)
            card_values = pairs[:2]
            if pairs[-1] == card_values[-1]:
                card_values.append(single_cards[0])
            else:
                card_values.append(max(single_cards[0], pairs[2]))

            return 2, card_values
        else:
            return None, None

    @staticmethod
    def check_three_of_a_kind(value_count):
        '''
        Checks for a three of a kind in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 3 ( the value of a three of a kind) and
        a list with the pairs and the two highest cards exluding the three of a kind
        '''
        if 3 in value_count:
            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 1:
                    single_cards.append(j + 1)
            card_values = [value_count.index(3) + 1,  single_cards[0], single_cards[1]]
            return 3, card_values
        else:
            return None, None

    @staticmethod
    def check_straight(value_count):
        ''' Checks for the highest straight in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 4 ( the value of a two pair) and
        the highest card in the straight'''
        n = 13
        if value_count[13] != 0:
            value_count[0] = 1
        for i in reversed(value_count):
            if n == 3:
                return None, None
            if i != 0:
                if value_count[n - 1] != 0:
                    if value_count[n - 2] != 0:
                        if value_count[n - 3] != 0:
                            if value_count[n - 4] != 0:
                                card_values = [n+1]
                                return 4, card_values
            n -= 1

    @staticmethod
    def check_flush(suit_count, suit_card_connector):
        ''' Checks for the highest flush in a pokerhand
        :param suit_count: number of cards of each suit
        :param suit_card_connector: list containing how many of each card with the most common suit
        is in the hand
        :return  None if no flush is found, else 5 ( the value of a flush) and a list of the five
         highest cards in the flush
        '''
        if max(suit_count) >= 5:
            card_values = []
            for j, card in reversed(list(enumerate(suit_card_connector))):
                if card:
                    card_values.append(j+1)
            return 5, card_values[:5]
        else:
            return None, None

    @staticmethod
    def check_full_house(value_count):
        ''' Checks for the best full house in a pokerhand
                 :param value_count: list containing the how many of each card is in the hand
                 :return  None if no full house is found, else 6 ( the value of a full house) and
                 a list with the three of a kind and the pair'''
        if 3 in value_count:
            card_values = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 3:
                    card_values.append(j+1)
            if len(card_values) == 2:
                return 6, card_values
            elif 2 in value_count:
                for j, data in reversed(list(enumerate(value_count))):
                    if data == 2:
                        card_values.append(j + 1)
                        return 6, card_values
            else:
                return None, None
        else:
            return None, None

    @staticmethod
    def check_four_of_a_kind(value_count):
        ''' Checks for a four of a kind in a pokerhand
                 :param value_count: list containing the how many of each card is in the hand
                 :return  None if no four of a kind is found, else 7 ( the value of a two pair) and
                 a list with the four of a kind and the highest card exluding the four of a kind
                 '''
        if 4 in value_count:
            for j, data in reversed(list(enumerate(value_count))):
                if data in range(1, 4):
                    card_values = [value_count.index(4)+1, j+1]
                    return 7, card_values
        else:
            return None, None



    @staticmethod
    def check_straight_flush(suit_card_connector, suit_count):
        ''' Checks for the highest straight flush in a pokerhand
        :param suit_count: number of cards of each suit
        :param suit_card_connector: list containing how many of each card with the most common suit
        is in the hand
        :return  None if no straight flush is found, else 8 ( the value of a straight flush) and
                 the highest card in the straight flush
        '''
        if max(suit_count) >= 5:
            if suit_card_connector[13]:
                suit_card_connector[0] = True
            for i, data in reversed(list(enumerate(suit_card_connector))):
                if i == 3:
                    return None, None
                if data != 0:
                    if suit_card_connector[i-1]:
                        if suit_card_connector[i-2]:
                            if suit_card_connector[i-3]:
                                if suit_card_connector[i-4]:
                                    card_values = [i+1]
                                    return 8, card_values
        else:
            return None, None


class PokerHand:
    '''Class to represent the pokerhands and making them comparable'''
    def __lt__(self, other):
        return (self.cardcombo, self.highcard) < (other.cardcombo, other.highcard)

    def __init__(self, cardcombo, highcard):
        self.highcard = highcard
        self.cardcombo = CardCombo(cardcombo)



