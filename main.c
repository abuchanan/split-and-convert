#include <zlib.h>
#include <stdio.h>
#include <string.h>
#include "kseq.h"

KSEQ_INIT(gzFile, gzread)

const int NUM_BASES_TO_STRIP = 10;

int main(int argc, char *argv[])
{
	gzFile fp;
	kseq_t *seq;
	int l;

	if (argc != 2) {
		fprintf(stderr, "Usage: %s <in.seq>\n", argv[0]);
		return 1;
	}

	fp = gzopen(argv[1], "r");
	seq = kseq_init(fp);

	while ((l = kseq_read(seq)) >= 0) {

		printf("name: %s\n", seq->name.s);
		printf("seq: %s\n", strndup(seq->seq.s + NUM_BASES_TO_STRIP, strlen(seq->seq.s)));
	}

	kseq_destroy(seq);
	gzclose(fp);

	return 0;
}
