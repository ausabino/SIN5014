CC=gcc

FFLAGS= -O3
MAIN	= objloaderelephant

$(MAIN)	: $(MAIN).o
	$(CC) $(FFLAGS) $(MAIN).o -o $(MAIN) -lm -lglut -lGL -lGLU

$(MAIN).o: $(MAIN).c
	$(CC) -c $(MAIN).c

clean:
	rm -f *.o

veryclean:
	rm -f $(MAIN)
	rm -f *.o
	rm -f *.*~
