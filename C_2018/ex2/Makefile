all: battleships.h battleships.c battleships_game.c
	gcc -Wextra -Wall -Wvla -std=c99 battleships.c battleships_game.c -o ex2

battleships: battleships.h battleships.c
	gcc -Wextra -Wall -Wvla -std=c99 -c battleships.c

clean:
	rm -rf *o ex2