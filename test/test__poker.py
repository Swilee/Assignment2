from nose.tools import assert_raises
import unittest
import poker


def test_math():
    assert 1 + 1 == 2
    assert 2 * 2 + 3 == 7



def test_PlayingCard():
    result = poker.KingCard
    assert type(result) == type(poker.PlayingCard)

def test_CardCombo():
    result = poker.CardCombo.straightflush
    assert result == 8

