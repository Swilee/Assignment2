from nose.tools import assert_raises
import poker


def test_math():
    assert 1 + 1 == 2
    assert 2 * 2 + 3 == 7


def test_PlayingCard():
    result = poker.KingCard(poker.Suit.Hearts)
    assert isinstance(result, poker.PlayingCard)


def test_CardCombo():
    assert poker.CardCombo.straightflush > poker.CardCombo.fourofakind
    assert poker.CardCombo.fourofakind > poker.CardCombo.fullhouse
    assert poker.CardCombo.fullhouse > poker.CardCombo.flush
    assert poker.CardCombo.flush > poker.CardCombo.straight
    assert poker.CardCombo.straight > poker.CardCombo.threeofakind
    assert poker.CardCombo.threeofakind > poker.CardCombo.twopair
    assert poker.CardCombo.twopair > poker.CardCombo.onepair
    assert poker.CardCombo.onepair > poker.CardCombo.highcard
    with assert_raises(TypeError):
        poker.NumberedCard(5, poker.Suit.Clubs) > poker.CardCombo.highcard

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


def test_twopair():
    hand = poker.PlayerHandModel()
    hand.give_card(poker.AceCard(poker.Suit.Spades))
    hand.give_card(poker.AceCard(poker.Suit.Diamonds))
    hand.give_card(poker.NumberedCard(10, poker.Suit.Clubs))
    hand.give_card(poker.NumberedCard(10, poker.Suit.Spades))
    hand.give_card(poker.NumberedCard(9, poker.Suit.Hearts))
    hand.give_card(poker.NumberedCard(5, poker.Suit.Clubs))
    hand.best_poker_hand([])
    result = poker.CardCombo.twopair

    assert result == hand.pokerhand.cardcombo


def test_pokerhand():
    result = poker.PokerHand(1, [2])
    assert issubclass(type(result.cardcombo), poker.Enum)

def test_full_round():
    '''Testing a full round where both players should hit a full house, making sure the PokerHand prioritize correctly
    and that "best_poker_hand" will return correctly. (all the functions of best_poker_hand can be tested the same way)
    '''
    player1 = poker.PlayerHandModel()
    player1.give_card(poker.AceCard(poker.Suit.Spades))
    player1.give_card(poker.AceCard(poker.Suit.Diamonds))

    player2 = poker.PlayerHandModel()
    player2.give_card(poker.KingCard(poker.Suit.Hearts))
    player2.give_card(poker.KingCard(poker.Suit.Diamonds))

    table = [poker.NumberedCard(5, poker.Suit.Clubs), poker.KingCard(poker.Suit.Clubs), poker.JackCard(poker.Suit.Diamonds),poker.JackCard(poker.Suit.Clubs), poker.JackCard(poker.Suit.Hearts)]

    player1.best_poker_hand(table)
    player2.best_poker_hand(table)
    assert player2.card_combo == poker.CardCombo.fullhouse
    assert player2.card_combo == player1.card_combo
    assert player1.pokerhand < player2.pokerhand



