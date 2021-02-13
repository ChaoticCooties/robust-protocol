OPTS:=-std=gnu99 -Wall -pedantic -Werror -Wextra -g

all: receiver sender

receiver: receiver.o errs.o
	gcc $(OPTS) -pthread -o receiver receiver.o errs.o

receiver.o:
	gcc $(OPTS) -c receiver.c

errs.o: errs.c errs.h
	gcc $(OPTS) -c errs.c

clean:
	rm *.o main
