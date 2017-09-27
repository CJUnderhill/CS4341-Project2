# CS4341-Project2
### Developed by Daniel Kim, Spyridon Antonatos, and Chad Underhill for WPI's CS4341 Course with Professor Ruiz.

## Compiling and running the program:

To compile the program, simply run the following commands:

`
`

Running the program is just as simple. Run the following:

`
`

## The utility function:

Our utility function is contained within both our evaluation function and our minimax/ab-pruning functions.

From the perspective of the minimax/ab-pruning function, we check every generated state of the board for terminal moves using a built-in check_terminal_state function within our Board class. This identifies spaces on the board in which a single move would end the game - both for us and our opponent - and assign a value of 100 for moves that would result in our agent winning, and a value of -100 for moves that would result in our agent losing. This value is passed back to the minimax/ab-pruning function, and the decision on which move to make is determined by that value.

From the perspective of the evaluation function, terminal states are identified by finding spaces that we could play on which contain four tiles of either our color or our opponent's color in a row. If an open space containing four of our color tiles in a row next to it exists, we assign a move there a value of 1000000 - denoting a winning move. If an open space containing four of our opponent's color tiles in a row next to it exists, we assign a move there a value of 100000. The difference in value assign is to ensure that we always take a winning move if we can; there's no point in blocking an opponent's winning move if we can just win the game before they can play.

## The evaluation function:

The evaluation function is based on a whitepaper detailing a Threat-Space Search in Gomoku. This paper can be found here: http://www.renju.nu/wp-content/uploads/sites/46/2016/09/Go-Moku.pdf. The idea is relatively simple - we evaluate each unfilled position on the board twice - once with the mindset of finding a strong move for ourselves (attacking), and once with the mindset of preventing the opponent from finding a strong move (defending). We evaluate up to five tiles in each direction of the position we're evaluating, assigning an exponentially higher positional value to each consecutive tile in a chain on these paths; as such, a potential move with three pre-exisitng tiles of ours on both the north and east sides will recieve a much higher positional "score" compared to a position with just three pre-existing tiles on any given side (or even fewer).

Beyond this, as detailed in the "utility function" section above, if we find a string of four tiles adjacent to an open space on the board, we identify that space as terminal and assign it a value of 1000000 - far outweighing the maximum score any other any other configuration might net. We assign terminal spaces for our opponent a value of 100000, which incentivizes our program to pick a winning space for us before blocking the opponent from winning.

Finally, we combine our two scores - attacking and defending - giving us a net evaluation that results in a maximally-strategic move that considers both benefits to us and detractors from our opponent.

## Heuristics and strategies:

Our heuristics are detailed in the two sections above. Our strategy revolves around "cutting off" our minimax/ab-pruning algorithm when it's reached a specified limit. This limit could be based on minimax tree depth, the number of nodes visited, or time consumption. Each iteration of our minimax function checks if it's within our cutoff limits. If the minimax function exceeds these limits, we kick the program out to our evaluation function - which quickly and effectively evaluates the board for each generated state of the minimax tree and determines the most strategic move to proceed with.

## The results:

# We need to answer these
-describe which tests you ran to try out your program. Did your program play against human players? Did your program play against itself? Did your program play against other programs? How did your program do during those games?
-describe the strengths and the weaknesses of your program.

## Why we chose our evaluation function and heuristics:

We chose our evaluation function methodology after researching some of the most effective solutions to a Gomoku board/game. Our research turned up a "Threat-Space Search" approach and we decided that would be an excellent way of evaluating any given Gomoku board configuration. Our heuristics within that - of evaluating moves that are strategic both offensively and defensively based on pre-existing tile placement and potential to create five-in-a-row combinations - was heavily influenced by the "Threat-Space Search" theory. Our minimax/ab-pruning heuristics follow the standard minimax/ab-pruning guidelines, simply evaluating positions based on win/loss results and preferring choices that result in more winning combinations than losing. By pruning out branches that we know will provide less strategic results, we increase the efficiency of our minimax algorithm significantly.
