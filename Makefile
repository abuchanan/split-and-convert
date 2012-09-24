all:kseq.h main.c
		$(CC) -g -O2 main.c -o strip-and-convert -lz

clean:
		rm -f *.o strip-and-convert
