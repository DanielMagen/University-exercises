CC=g++
CXX=g++
RANLIB=ranlib

LIBSRC=MapReduceFramework.cpp MapReduceFramework.h MapReduceClient.h Barrier.cpp Barrier.h JobContext.cpp JobContext.h ShuffleThreadContext.cpp ShuffleThreadContext.h ThreadContext.cpp ThreadContext.h GlobalVariables.cpp GlobalVariables.h
LIBOBJ=$(LIBSRC:.cpp=.o)

INCS=-I.
CFLAGS = -Wall -std=c++11 -g -pthread $(INCS)
CXXFLAGS = -Wall -std=c++11 -g -pthread $(INCS)

FRAMEWORKLIB = libMapReduceFramework.a
TARGETS = $(FRAMEWORKLIB)

TAR=tar
TARFLAGS=-cvf
TARNAME=ex3.tar
TARSRCS=$(LIBSRC) Makefile README

all: $(TARGETS)

$(TARGETS): $(LIBOBJ)
	$(AR) $(ARFLAGS) $@ $^
	$(RANLIB) $@

clean:
	$(RM) $(TARGETS) $(FRAMEWORKLIB) $(OBJ) $(LIBOBJ) *~ *core

depend:
	makedepend -- $(CFLAGS) -- $(SRC) $(LIBSRC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)
