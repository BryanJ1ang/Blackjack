# Blackjack Web Game
Please visit <https://bryanjiang.itch.io/blackjack> to try the game

## The Game
Blackjack is a popular casino card game pitting players against the dealer. The gameplay revolves around both sides attempting to have their cards sum up as close to 21 as possible without going over. Currently, the web app allows the user to play three hands at once. At the start, you will be prompted to select the amount of money to bet for each hand. 

<br/>

![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/538f1d9e-044d-4c12-8360-6b94f6e4612a)

<br/>

Once all bets have been placed, the game starts with two cards being dealt to each player and the dealer. One of the dealer's card is face down during this stage of the game. Then in a clock-wise rotation, players are able to choose from a range of commands. The main commands are "HIT", which deals one more card and "STAND", which ends the player's turn with their current total. 
<br/>
![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/7d97dec0-862d-45b6-8a59-e3c9c18522ab)
<br/>

Once each player has finished their turn, the dealer flips their face down card and then they must keep 'hitting' until  their hand value is at least 17. After that, each player either wins or loses their bets accordingly and a new round can begin.
<br/>
![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/cf9f5968-a89f-4aec-9faa-979890b5594e)
<br/>

## Blackjack Rules
#### Player Win Conditions: 
* Value of  theplayer's hand is  is greater than the dealer’s 
* Value of the dealer's hand is greater than 21 and the player's hand is not

#### Dealer Win Conditions:
* Value of the player's hand exceeds 21
* Value of the dealer's hand is greater than the player

#### Card Values:
* Cards from 2-10 are worth their face values
* Jacks, Queens and Kings all are worth 10
* Aces are worth either 1 or 11 depending on whichever is more beneficial to the owner's hand

## Inspiration
Back in high school, my friends and I used to play card games all the time during lunch time. Games such as Big Two, Crazy Eights and even Blackjack. Though when we played, we used rocks and erasers as our money. This project could be useful for people looking to:
* learn the rules of the game before betting actual real money
* practice [basic strategy](https://www.blackjackapprenticeship.com/blackjack-strategy-charts/) (the statistically most optimal play for each combination of hand)
* simulate probabilities or practice card counting

## The Process
This project was coded in Python, using Pygame for the GUI and then converted into WebAssembly using Pygbag for web deployment. The core of the project was built around a module that contains both a Card and Deck class. These classes offer methods for shuffling, inserting, and drawing cards, making it adaptable for creating other card games.

One of the most challenging aspects of this project was managing the GUI components, as they were coded within a single module. For future iterations and other projects, I would definitely split the GUI into multiple modules to enhance readability and reduce code coupling. Additionally, the web-based version of the game experienced frequent freezing because card images were fetched constantly. As such, this was addressed by caching all of the image assets in a dictionary at startup.


## Known Bugs
* Deck has the same shuffle between sessions. (i.e. player 1 will always be dealt a 3 and 2 in the first round) likely an
  stemming from compiltion into WASM
* SPLIT Button not yet implemented properly

