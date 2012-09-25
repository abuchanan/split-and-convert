#!/bin/bash

rm -rf stripped-and-converted/
rm -rf log
annotate-output python2.7 ../run.py test.fastq.gz test2.fastq.gz > log
gunzip stripped-and-converted/*
diff expected.fasta stripped-and-converted/test.fasta
diff expected.fasta stripped-and-converted/test2.fasta
