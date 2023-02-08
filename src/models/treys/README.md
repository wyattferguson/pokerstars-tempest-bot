Treys

A pure Python poker hand evaluation library

https://github.com/ihendley/treys

Treys is a Python 3 port of Deuces based on the initial work in msaindon’s fork. Deuces was written by Will Drevo for the MIT Pokerbots Competition.

Treys is lightweight and fast. All lookups are done with bit arithmetic and dictionary lookups. That said, Treys won’t beat a C implemenation (~250k eval/s) but it is useful for situations where Python is required or where bots are allocated reasonable thinking time (human time scale).

Treys handles 5, 6, and 7 card hand lookups. The 6 and 7 card lookups are done by combinatorially evaluating the 5 card choices.
