import random

class playingCard:
    
    def __init__(self, value_string=None, suit_string=None):
        self.suit_string = suit_string
        self.value_string = value_string
        
        self.value = None
        self.suit = None
        self.value_symbol = None
        
        if self.suit_string or self.value_string is not None:
            self.parseCard()
    
    def getCard(self):
        if isinstance(self.value_string, int):
            return f"{self.value_string} of {self.suit_string.title()}"
        else:
            return f"{self.value_string.title()} of {self.suit_string.title()}"
    
    def getCardSymbol(self):
        return self.__str__()
    
    def parseCard(self):
        if self.suit_string.lower() == 'spades' or self.suit == '♤':
            self.suit = '♤'
            self.suit_string = 'spades'
            
        if self.suit_string.lower() == 'clubs' or self.suit == '♧':
            self.suit = '♧'
            self.suit_string = 'clubs'
            
        if self.suit_string.lower() == 'hearts' or self.suit == '♥':
            self.suit = '♥'
            self.suit_string = 'hearts'
            
        if self.suit_string.lower() == 'diamonds' or self.suit == '♦':
            self.suit = '♦'
            self.suit_string = 'diamonds'
        
        if isinstance(self.value_string, int):
            self.value = int(self.value_string)
            if self.value == 11:
                self.value_symbol = "J"
                self.value_string = 'jack'
            if self.value == 12:
                self.value_symbol = "Q"
                self.value_string = 'queen'
            if self.value == 13:
                self.value_symbol = "K"
                self.value_string = 'king'
            if self.value == 14:
                self.value_symbol = "A"
                self.value_string = 'ace'

        else:
            if self.value_string.upper() == 'J' or self.value_string.lower() == 'jack':
                self.value = 11
                self.value_symbol = "J"
                self.value_string = 'jack'

            if self.value_string.upper() == 'Q' or self.value_string.lower() == 'queen':
                self.value = 12
                self.value_symbol = "Q"
                self.value_string = 'queen'

            if self.value_string.upper() == 'K' or self.value_string.lower() == 'king':
                self.value = 13
                self.value_symbol = "K"
                self.value_string = 'king'

            if self.value_string.upper() == 'A' or self.value_string.lower() == 'ace':
                self.value = 14
                self.value_symbol = "A"
                self.value_string = 'ace'
        
    def __str__(self):
        if self.value <= 10:
            return f"{self.value_string}{self.suit}"
        else:
            return f"{self.value_symbol}{self.suit}"
    
    def __repr__(self):
        if self.value <= 10:
            return f"{self.value_string}{self.suit}"
        else:
            return f"{self.value_symbol}{self.suit}"
        

class deckOfCards(playingCard):
    
    def __init__(self, deck=None):
        super().__init__()
        
        self.suits = ['spades', 'clubs', 'hearts', 'diamonds']
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        
        if deck is not None:
            self.cards = deck
        else:
            self.cards = {}
        
        for suit in self.suits:
            for value in self.values:
                temp = playingCard(value, suit)
                temp.parseCard()
                self.cards[temp.getCard()] = temp
        
    def getCardsInDeck(self):
        return self.cards.items()
        
    def getRandomCard(self, num=1):
        hand = {}
        
        for card in range(0,num):
            suit = random.choice(self.suits)
            value = random.choice(self.values)
            if value == 'J':
                value = 'Jack'
            if value == 'Q':
                value = 'Queen'
            if value == 'K':
                value = 'King'
            if value == 'A':
                value = 'Ace'
            
            try:
                hand[f"{value} of {suit.title()}"] = self.cards.pop(f"{value} of {suit.title()}")
            except KeyError:
                print("Re-drawing")
            
        return hand
    
    def shuffleCards(self, deck=None):
        newHand = {}
        
        if deck is not None:
            oldHand = deck
        else:
            oldHand = self.cards
        
        while oldHand:
            
            for card in range(0, len(oldHand)):
                suit = random.choice(self.suits)
                value = random.choice(self.values)
                if value == 'J':
                    value = 'Jack'
                if value == 'Q':
                    value = 'Queen'
                if value == 'K':
                    value = 'King'
                if value == 'A':
                    value = 'Ace'
                
                try:
                    newHand[f"{value} of {suit.title()}"] = oldHand.pop(f"{value} of {suit.title()}")
                except KeyError:
                    pass

            
        return deckOfCards(newHand)
        
        
class ShuffleWar(deckOfCards):
    """ Where each round is randomly shuffled! And thats a feature, not a bug. """
    
    def __init__(self):
        super().__init__()
        
        self._create_players()
        self.isRunning = True
        self._run_game()
            
    def _create_players(self):
        self._prompt_players()
        self._assign_cards()
    
    def _run_game(self):
        # main while loop, 
        while self.isRunning:
            self._draw_cards()
            self._compare_values()
            if (len(self.player_one['hand'])) != 0 and (len(self.player_two['hand'])) != 0:
                ask_again = input("Again? (y/n)")
                if ask_again == 'y':
                    continue
                else:
                    self.isRunning = False
            elif len(self.player_one['hand']) == 0:
                print("\nPlayer 2 wins it all!\n")
                self.isRunning = False
                
            elif len(self.player_two['hand']) == 0:
                print("\nPlayer 1 wins it all!\n")
                self.isRunning = False
            
    
    def _assign_cards(self):
        self.deck = deckOfCards()
        self.deck = self.deck.shuffleCards()
        
        self.player_one['hand'] = dict(list(self.deck.cards.items())[len(self.deck.cards)//2:])
        self.player_two['hand'] = dict(list(self.deck.cards.items())[:len(self.deck.cards)//2])
    
    def _prompt_players(self):
        self.player_one = {}
        self.player_two = {}
        
        self.player_one['name'] = input("Please enter player 1: ")
        self.player_two['name'] = input("Please enter player 2: ")
        
    def _draw_cards(self):
        draw_num_p1 = random.randint(0, len(list(self.player_one['hand']))-1)
        draw_num_p2 = random.randint(0, len(list(self.player_two['hand']))-1)
        
        self.drawnCardP1 = list(self.player_one['hand'])[draw_num_p1]
        self.drawnCardP2 = list(self.player_two['hand'])[draw_num_p2]
        
        self.drawnCardP1 = self.player_one['hand'][self.drawnCardP1]
        self.drawnCardP2 = self.player_two['hand'][self.drawnCardP2]
        
        print(f"\nPlayer one: {self.drawnCardP1}")
        print(f"Player two: {self.drawnCardP2}\n")
    
    def _compare_values(self):
    
        if self.drawnCardP1.value > self.drawnCardP2.value:

            print("\nPlayer 1 wins!\n")
            card = self.player_two['hand'].pop(self.drawnCardP2.getCard())
            self.player_one['hand'][self.drawnCardP2.getCard()] = card
            print(f"P1: {len(self.player_one['hand'])}")
            print(f"P2: {len(self.player_two['hand'])}\n")
            return 'P1'

        elif self.drawnCardP1.value < self.drawnCardP2.value:
            print("\nPlayer 2 wins!\n")
            card = self.player_one['hand'].pop(self.drawnCardP1.getCard())
            self.player_two['hand'][self.drawnCardP1.getCard()] = card
            print(f"P1: {len(self.player_one['hand'])}")
            print(f"P2: {len(self.player_two['hand'])}\n")
            return 'P2'

        else:
            print("\nWar!\n")

            print(f"P1: {len(self.player_one['hand'])}")
            print(f"P2: {len(self.player_two['hand'])}\n")
            self.pool = []
            for i in range(0,3):
                self._draw_cards()
                self.pool.append(self.drawnCardP1)
                self.pool.append(self.drawnCardP2)

                self.player_one['hand'].pop(self.drawnCardP1.getCard())
                self.player_two['hand'].pop(self.drawnCardP2.getCard())

            print(len(self.player_one['hand']))
            print(len(self.player_two['hand']))

            self._draw_cards()
            victory = self._compare_values()
            if victory == 'P1':
                print("\nP1 Wins the War!\n")
                for card in self.pool:
                    self.player_one['hand'][card.getCard()] = card
            elif victory == 'P2':
                print("\nP2 Wins the War!\n")
                for card in self.pool:
                    self.player_two['hand'][card.getCard()] = card


            print(self.pool)
            print(f"\nP1: {len(self.player_one['hand'])}")
            print(f"P2: {len(self.player_two['hand'])}\n")