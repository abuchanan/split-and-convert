from __future__ import print_function

import argparse
import itertools
import gzip
import logging
import multiprocessing
import os
import subprocess
import time


log = multiprocessing.log_to_stderr()
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('fastq', nargs='+')

parser.add_argument('--dry-run', action='store_true')


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def run_strip_and_convert(input_path, output_path):

    input = gzip.open(input_path)
    output = gzip.open(output_path, 'wb')

    for header, seq, strand, quality in grouper(4, input):
        header = header.strip()
        seq = seq.strip()
        header = '>' + header[1:]
        seq = seq[10:]
        print(header, seq, sep='\n', file=output)

    input.close()
    output.close()

    log.info('Completed: {0} > {1}'.format(input_path, output_path))


if __name__ == '__main__':
    args = parser.parse_args()

    num_processes = min(7, len(args.fastq))
    pool = multiprocessing.Pool(processes=num_processes)

    for input_path in args.fastq:

        dir_path, file_name = os.path.split(input_path)
        file_name = file_name.replace('fastq', 'fasta')
        output_path = os.path.join(dir_path, 'stripped-and-converted', file_name)
        output_dir = os.path.dirname(output_path)

        if args.dry_run:
            log.info('Dry-run completed: {0} > {1}'.format(input_path, output_path))
        else:
            # ensure that the full path to the output file exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # DEBUG
            #run_strip_and_convert(input_path, output_path)

            pool.apply_async(run_strip_and_convert, (input_path, output_path))

    pool.close()
    pool.join()
