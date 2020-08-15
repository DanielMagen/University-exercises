CC = g++
CCFLAGS = -c -Wall -Wextra -std=c++17 -pthread -g
LDFLAGS = -lm

# add your .c files here  (no file suffixes)
CLASSES = Vector3D Matrix3D ex1

# Prepare object and source file list using pattern substitution func.
OBJS = $(patsubst %, %.o,  $(CLASSES))
SRCS = $(patsubst %, %.cpp, $(CLASSES))

all: $(OBJS) libalg.a
	$(CC) $(OBJS) $(LDFLAGS) -L. -lalg -o ex1

%.o: %.cpp
	$(CC) $(CCFLAGS) $*.cpp

LIBOBJECTS = Vector3D.o Matrix3D.o

libalg.a: ${LIBOBJECTS}
	ar rcs libalg.a ${LIBOBJECTS}
depend:
	makedepend -- $(CCFLAGS) -- $(SRCS)
# DO NOT DELETE
