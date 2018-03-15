from nose.tools import assert_raises
import unittest
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

def test_best_poker_hand():
    hand = poker.PlayerHandModel()
    deck = poker.Deck()
    hand.best_poker_hand(deck.deck)
    assert hand.pokerhand.cardcombo == poker.CardCombo.straightflush


def test_pokerhand():
    result = poker.PokerHand(1,[2])
    assert issubclass(type(result.cardcombo), poker.Enum)