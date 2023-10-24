# Blackjack Web Game
Please visit <https://bryanjiang.itch.io/blackjack> to try the game

## The Game
Blackjack is a popular casino card game pitting players against the dealer. The gameplay revolves around both sides attempting to have cards sum up as close to 21 as possible without going over. Currently, the web app allows the user to play three hands at once. You will be prompted to select the amount of money to bet for each hand. 

<br/>
![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/68ec5d57-f168-4a9a-bb8e-030bdbf30ea7)
<br/>

Once all bets have been placed, the game starts with each player as well as the dealer each dealt two cards. One of the dealer's card is face down during this stage of the game. Then in a clock-wise rotation, player's are able to choose from a range of commands. HIT deals one more card while STAND ends the player's turn with their current total. 
<br/>
![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/7d97dec0-862d-45b6-8a59-e3c9c18522ab)
<br/>

Once each player has finished their turn, the dealer flips their face down card and then must keep 'hitting' until either their hand is at least 17. After that, each player either wins or loses their bets accordingly and a new round can begin.
<br/>
![image](https://github.com/BryanJ1ang/Python-Blackjack/assets/134325602/cf9f5968-a89f-4aec-9faa-979890b5594e)
<br/>

## Blackjack Rules
#### Player Win Conditions: 
* if player has  a hand value that is greater than the dealer’s hand value
* if the dealer's hand goes over 21 and the player's hand does not

#### Dealer Win Conditions:
* Player's hand value exceeds 21
* Dealer's hand value is greater than player's

#### Card Values:
* Cards from 2-10 are their face values
* Jacks, Queens and Kings all have the value of 10
* Aces are worth either 1 or 11 depending on whichever is more beneficial to the owner's hand

## Inspiration
Back in high school, my friends and I used to play card games all the time during lunch time. Games such as Big Two and Crazy Eights gave me fond memories but Blackjack in particular was unforgettable.
We used rocks and erases as our money and just had a blast pretending we were winning big money. As such, this project pays a bit of homage to my high school days as well as letting me develop my Python and general programming skills.

## The Process
The project is coded in Python, using Pygame for the GUI and then converted into WebAssembly using Pygbag for web deployment. The core of the project is built around a module that contains both a Card and Deck class. These classes offer methods for shuffling, inserting, and drawing cards, making it adaptable for creating other card games.

One of the most challenging aspects of this project was managing the GUI components, as they were coded within a single module. For future iterations and other projects, I would definitely split the GUI into multiple modules to enhance readability and reduce code coupling. Additionally, the web-based version of the game experienced frequent freezing because card images were fetched constantly. As such, this was addressed by caching all of the image assets in a dictionary at startup.


## Known Bugs
* Deck has the same shuffle between sessions. (i.e. player 1 will always be dealt a 3 and 2 in the first round) likely an
  stemming from compiltion into WASM
* SPLIT Button not yet implemented properly

