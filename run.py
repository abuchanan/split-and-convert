from glob import glob
import logging
import multiprocessing
import os
import subprocess
import time


log = multiprocessing.log_to_stderr()
log.setLevel(logging.INFO)


def run_strip_and_convert(input_path, output_path):

    cmd = 'strip-and-convert {0} | gzip > {1}'.format(input_path, output_path)
    try:
        subprocess.check_output(cmd, shell=True)
        log.info('Completed: {0} > {1}'.format(input_path, output_path))
    except subprocess.CalledProcessError, e:
        log.error('Error: {0}'.format(e.output))


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=7)

    for file_path in glob('../original/**/*.fastq.gz'):
        # build an output file path using the input file path
        # e.g.
        #  ../original/sample_name/read_file
        #  becomes 
        #  ./sample_name/read_file
        dir_path, file_name = os.path.split(file_path)
        _, dir_name = os.path.split(dir_path)
        output_path = os.path.join(dir_name, file_name)

        # ensure that the full path to the output file exists
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        pool.apply_async(run_strip_and_convert, (file_path, output_path))

    pool.close()
    pool.join()
