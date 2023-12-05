# advent_of_code
Solvers for Advent of Code puzzles.

## Win Condition
I'm usually just going for completion, not high score when it comes to AoC. It's
a busy time of year, and often I won't get to work on puzzles the night they
come out. I'll be happy if I get through all or most of the puzzles before the
new year, and especially happy if I pick up some new ideas and techniques along
the way.

## Readability
I try to write code for AoC that's at least semi-readable, often with some type
annotations in the mix. I don't see this as slowing down my overall software
process. On the contrary, keeping the code semi-readable is sometimes the only
way I can actually keep the problem straight enough in my head to have a chance
at solving it at all. Being able to point the linter at the code can sometimes
avoid those time where it takes waaaaayyy to long to see that small typo that's
causing a weird wrong result. Part of the exercise for me is finding the sweet
spot where I'm getting good value from readability without overdoing it too
much.

In general I use `black` to format my Python code (as of 2023).

## Design Patterns
Often I find that if I pick good patterns and abstractions for part 1, part 2
will follow naturally. Sometimes this means part 1 takes me a little longer but
part 2 is done in seconds. This feels good to me because it reassures me that
I'm picking extensible, maintainable patterns when I write code. Learning to hit
this condition more consistently is a big part of the value of doing AoC for me.
Of course it doesn't always work out so smoothly. Sometimes I'm very wrong about
the direction the problem was going, and part 2 ends up full-jank.

## Usage
To run the solvers, check the docstrings within each year's directory. I play
around with different patterns from year to year. Some years have stand-alone
scripts, some have a main entry point that can import and run the day's solver.