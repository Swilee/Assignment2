from nose.tools import assert_raises
import unittest
import numpy as np
import poker


def test_math():
    assert 1 + 1 == 2
    assert 2 * 2 + 3 == 7


def test_PlayingCard():
    result = poker.KingCard(poker.Suit.Hearts)
    assert isinstance(result, poker.PlayingCard)


def test_CardCombo():
    assert poker.CardCombo.straightflush > poker.CardCombo.fourofakind


def test_deck():
    result = poker.Deck()
    assert result.deck.size == 52
    result.take_top_card()
    assert result.deck.size == 51
    



def test_deck_take_top_card():
    all_cards = poker.Deck()
    top_card = all_cards.deck[-1]
    result = all_cards.take_top_card()
    assert result == top_card



def test_best_poker_hand():
    hand = poker.PlayerHandModel()
    deck = poker.Deck()
    hand.best_poker_hand(deck.deck)
    assert hand.pokerhand.cardcombo == poker.CardCombo.straightflush


def test_a_poker_hand():
    hand = poker.PlayerHandModel()
    hand.give_card(poker.AceCard(poker.Suit.Spades))
    hand.give_card(poker.QueenCard(poker.Suit.Hearts))
    hand.give_card(poker.QueenCard(poker.Suit.Clubs))
    hand.give_card(poker.JackCard(poker.Suit.Clubs))
    hand.give_card(poker.NumberedCard(8, poker.Suit.Spades))
    hand.give_card(poker.NumberedCard(4, poker.Suit.Hearts))
    hand.give_card(poker.NumberedCard(4, poker.Suit.Spades))

    hand.best_poker_hand(hand.cards)
    print(hand.cards)
    result = poker.CardCombo.twopair
    print(result)
    print(hand.pokerhand.cardcombo)
    assert result == hand.pokerhand.cardcombo


def test_pokerhand():
    result = poker.PokerHand(1, [2])
    assert issubclass(type(result.cardcombo), poker.Enum)
