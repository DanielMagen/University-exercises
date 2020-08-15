CC = g++
CCFLAGS = -c -Wall -std=c++17 -pthread -g
LDFLAGS = -lm

# add your .cpp files here  (no file suffixes)
CLASSES = AuthorCompare ex2

# Prepare object and source file list using pattern substitution func.
OBJS = $(patsubst %, %.o,  $(CLASSES))
SRCS = $(patsubst %, %.cpp, $(CLASSES))

all: $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o find_the_author

%.o: %.cpp
	$(CC) $(CCFLAGS) $*.cpp

depend:
	makedepend -- $(CCFLAGS) -- $(SRCS)
# DO NOT DELETE
