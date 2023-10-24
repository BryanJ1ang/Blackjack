# Blackjack Web Game
Please visit <https://bryanjiang.itch.io/blackjack> to try the game

## Inspiration
Back in high school, my friends and I used to play card games all the time during lunch time. Games such as Big Two and Crazy Eights gave me fond memories but Blackjack in particular was unforgettable.
We used rocks and erases as our money and just had a blast pretending we were winning big money. As such, this project pays a bit of homage to my high school days as well as letting me develop my Python and general programming skills.


## The Process
The entire project is written in Python with the Pygame library used for the GUI and then converted into WebAssembly using Pygbag for deploying. Project can be expanded to
include other card games as it is comprised of a Module containing a Card and Deck class with methods for shuffling, inserting and drawing cards.

## Known Bugs
* Deck has the same shuffle between sessions. (i.e. player 1 will always be dealt a 3 and 2 in the first round)
* SPLIT Button not yet implemented properly, currently does nothing

