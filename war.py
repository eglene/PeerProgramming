import random
import time

CARD_VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

CARD_TYPE = {
    'Diamonds': 0,
    'Hearts': 2,
    'Spades': 4, 
    'Clubs': 8
}

class Card:
    def __init__(self, type: str, name: str):
        if type not in CARD_TYPE:
            raise ValueError
        if name not in CARD_VALUES:
            raise ValueError
        
        self.__type = type
        self.__name = name
        # self._value = CARD_VALUES[name]

    @property
    def type(self):
        """Property respresenting the house of the card.

        Check CARD_TYPE for house of card names under keys and numercial values.
        
        Returns
        -------
        str
            the house of the card.
        """
        return self.__type

    @property
    def type_value(self):
        """Property representing the house of the card numerical value

        Check CARD_TYPE for house of card names under keys and numercial values.
        
        Returns
        -------
        int
            an int representing the house of card numerical value.
        """
        return CARD_TYPE[self.__type]

    @property
    def name(self):
        """Property representing the card 'name', e.g., name could be 2 or Q or A ...

        Check CARD_VALUES for card names under keys and numercial values.

        Returns
        -------
        str
            the card name represented as string
        """
        return self.__name
    
    @property
    def value(self):
        """Property representing the numerical value of the card.

        Check CARD_VALUES for card names under keys and numercial values.

        Returns
        -------
        int
            an int 2-14 representing the card numerical value.
        """
        return CARD_VALUES[self.__name]
    
    def __str__(self) -> str:
        return f'{self.name} of {self.type}'

class CardsDeck:
    def __init__(self):
        self.__cards: list[Card] = []

        for type in CARD_TYPE:
            for name in CARD_VALUES:
                self.__cards.append(Card(type, name))

        
        self.shuffle()

    @property
    def cards(self):
        return self.__cards

    def shuffle(self):
        random.shuffle(self.__cards)

class WarGame:
    def __init__(self, max_rounds=100):
        self.__rounds = 0
        self.__max_rounds = max_rounds
        self.__ended = False
        deck = CardsDeck()

        self.first_pile = deck.cards[:26]
        self.second_pile = deck.cards[26:]

    @property
    def rounds(self):
        return self.__rounds
    
    @property
    def ended(self):
        return self.__ended

    def play_round(self):
        # - Both players simultaneously reveal the top card from their pile.
        # - The player with the higher card value wins both cards and adds them to the bottom of their pile.
        # - If the cards are of equal value (a "war" situation), each player places three cards face-down
        #   and then reveals a fourth card. The player with the higher fourth card wins all the cards in that round.
        # - If there's another tie, the process continues with another "war."
        if self.__rounds < self.__max_rounds:
            self.__rounds += 1
            
            if self.first_pile and self.second_pile:
                print(f'Round {self.__rounds} (first: {len(self.first_pile)}, second: {len(self.second_pile)}):')
                # draw one card from the top of each pile
                first_card = self.first_pile.pop(0) # Instead of self.first_pile[0], which doesn't remove the card
                second_card = self.second_pile.pop(0)

                self.compare_cards_and_add(
                    first_card,
                    second_card,
                    [first_card, second_card])
            else:
                self.declare_winner()
        else:
            self.declare_winner()
            
    def declare_winner(self):
        self.__ended = True
        if len(self.first_pile) > len(self.second_pile):
            print(f'First player wins with {len(self.first_pile)} cards!!')
        elif len(self.first_pile) < len(self.second_pile):
            print(f'Second player wins with {len(self.second_pile)} cards!!')
        else:
            print(f'Tie no player wins the game better luck next time.')

    def compare_cards_and_add(
            self, first_card: Card, second_card: Card, cards: list[Card]):
        """
        A recursive function that compares two cards and adds the cards
        on table to the bottom of the winner's pile

        Parameters
        ----------
        first_card : Card
            the card of the first player to compare
        second_card : Card
            the card of the second player to compare
        cards : list[Card]
            a list that keeps track of the cards that has been drawn to the table.
        """
        if first_card.value > second_card.value:
            self.first_pile.extend(cards) # Append only accepts one item even a list adds as a seperate list
            print(f'First player takes the round taking {len(cards)} cards.')
        elif first_card.value < second_card.value:
            self.second_pile.extend(cards)
            print(f'Second player takes the round taking {len(cards)} cards.')
        else: # a tie
            first_draw = []
            second_draw = []
            for _ in range(4):
                if self.first_pile:
                    first_draw.append(self.first_pile.pop(0))
                if self.second_pile:    
                    second_draw.append(self.second_pile.pop(0))

            cards.extend(first_draw)
            cards.extend(second_draw)

            if len(first_draw) == 4 and len(second_draw) == 4:
                print('Tie')
                self.compare_cards_and_add(
                    first_draw[-1],
                    second_draw[1],
                    cards)
            elif len(first_draw) > len(second_draw):
                self.first_pile.extend(cards)
                print('Tie, but second player has no more cards.')
            else:
                self.second_pile.extend(cards)
                print('Tie, but first player has no more cards.')


game = WarGame(50)
while not game.ended:
    game.play_round()
    time.sleep(1)
