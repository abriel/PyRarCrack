"""
Bruteforce attack for .rar using unrar.

V: 0.0.2.4

Based on:
http://stackoverflow.com/questions/11747254/python-brute-force-algorithm
http://www.enigmagroup.org/code/view/python/168-Rar-password-cracker
http://rarcrack.sourceforge.net/
"""
from argparse import ArgumentParser
from itertools import chain, product
from functools import reduce
from operator import add, mul
from os.path import exists
from os import cpu_count, get_terminal_size
from sys import stdout
from time import sleep
from string import printable
from datetime import datetime, timedelta
from multiprocessing import Pool
from threading import Thread, Event
from rarcracklib import give_a_try

chars = (
    printable
    + 'ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌìÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß'
)

parser = ArgumentParser(description='Python combination generator to unrar')
parser.add_argument(
    '--start',
    help='Number of characters of the initial string [1 -> "a", 2 -> "aa"]',
    type=int,
)

parser.add_argument(
    '--stop',
    help='Number of characters of the final string [3 -> "ßßß"]',
    type=int,
)

parser.add_argument(
    '--verbose', help='Show combintations', default=False, required=False
)

parser.add_argument(
    '--alphabet',
    help='alternative chars to combinations',
    default=chars,
    required=False,
)

parser.add_argument(
    '--advanced-alphabet',
    help='a file contains the own alphabet for a password char (per a line)',
    default=None,
    required=False
)

parser.add_argument('--file', help='.rar file [file.rar]', type=str)

parser.add_argument('--processes', help='number of workers', default=cpu_count()-1, type=int)

parser.add_argument('--no-mt', help='do not use multiprocessing', action='store_true')

args = parser.parse_args()


def generate_combinations(alphabet, length, start=1):
    """Generate combinations using alphabet."""
    yield from (
        ''.join(string)
        for string in chain.from_iterable(
            product(alphabet, repeat=x) for x in range(start, length + 1)
        )
    )

def advanced_generator(positional_alphabet=[]):
    if not positional_alphabet:
        return positional_alphabet

    head = positional_alphabet[0]
    tail = positional_alphabet[1:]

    if tail:
        for head_e in head:
            for tail_e in advanced_generator(tail):
                yield head_e + tail_e
    else:
        yield from head

def total_combinations(alphabet, length, start=1):
    return reduce(add, (pow(len(alphabet), x) for x in range(start, length + 1)))

def give_a_try_worker(password):
    return give_a_try(give_a_try_worker.file, password)

def progress_report():
    stop = False

    while True:
        elapsed_time = datetime.now() - progress_report.start_time

        try:
            speed = progress_report.tested_combinations // elapsed_time.seconds
        except ZeroDivisionError:
            speed = 1

        try:
            estimated_time = timedelta(seconds=((progress_report.total_combinations - progress_report.tested_combinations) // speed))
        except OverflowError:
            estimated_time = 'infinite'
        except ZeroDivisionError:
            estimated_time = 'Nan'

        stdout.write(
            '\r{} % tested, {} comb/s, ELAPS {}, ETA {}'.format(
              round(progress_report.tested_combinations / progress_report.total_combinations * 100, 2),
              speed,
              str(elapsed_time).split('.')[0],
              estimated_time
            ).ljust(get_terminal_size().columns)
        )

        if stop: break

        if progress_report.stop_event.wait(timeout=6): stop = True


if __name__ == '__main__':
    if not exists(args.file):
        raise FileNotFoundError(args.file)

    if args.advanced_alphabet:
        alphabet_per_pchar = [list(line) for line in open(args.advanced_alphabet).read().split()]
        alphabet_generator = advanced_generator(alphabet_per_pchar)
        progress_report.total_combinations = reduce(mul, (len(x) for x in alphabet_per_pchar))
    else:
        if args.stop < args.start:
            raise Exception('Stop number is less than start')

        alphabet_generator = generate_combinations(
            args.alphabet, args.stop, args.start
        )
        progress_report.total_combinations = total_combinations(args.alphabet, args.stop, args.start)

    print(f'Loaded engine: {give_a_try.engine_name}')

    progress_report.start_time = datetime.now()
    progress_report.tested_combinations = 0
    progress_report.stop_event = Event()

    report_thread = Thread(target=progress_report)
    report_thread.start()

    if args.no_mt:
        for combination in alphabet_generator:
            if args.verbose:
                print(f'Trying: {combination}')

            if (correct_password := give_a_try(args.file, combination)):
                print(f'Password found: {correct_password}')
                break

            progress_report.tested_combinations += 1

    else:
        give_a_try_worker.file = args.file

        with Pool(processes=args.processes) as pool:
            for correct_password in pool.imap_unordered(
                give_a_try_worker,
                alphabet_generator,
                100
            ):
                if correct_password:
                    print(f'Password found: {correct_password}')
                    break

                progress_report.tested_combinations += 1

            pool.terminate()

    progress_report.stop_event.set()
