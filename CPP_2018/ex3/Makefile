CC = g++
CCFLAGS = -Wall -Wextra -std=c++17 -pthread -g
ARG = 500

all: run

run: timeChecker
	./timeChecker $(ARG)

timeChecker: TimeChecker.o Complex.o
	$(CC) $(CCFLAGS) Complex.o TimeChecker.o -o timeChecker

Matrix: Matrix.hpp.gch

Matrix.hpp.gch: Matrix.hpp Complex.h
	$(CC) $(CCFLAGS) Matrix.hpp -o Matrix.hpp.gch

TimeChecker.o: TimeChecker.cpp Matrix.hpp
	$(CC) $(CCFLAGS) -c TimeChecker.cpp

Complex.o: Complex.cpp Complex.h
	$(CC) $(CCFLAGS) -c Complex.cpp

clean:
	rm -f *.o timeChecker Matrix.hpp.gch