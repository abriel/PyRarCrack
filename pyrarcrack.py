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
from os.path import exists
from os import cpu_count
from string import printable
from time import time
from multiprocessing import Pool
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


def give_a_try_worker(password):
    return give_a_try(give_a_try_worker.file, password)


if __name__ == '__main__':
    if not exists(args.file):
        raise FileNotFoundError(args.file)

    if args.stop < args.start:
        raise Exception('Stop number is less than start')

    print(f'Loaded engine: {give_a_try.engine_name}')

    start_time = time()

    if args.no_mt:
        for combination in generate_combinations(
            args.alphabet, args.stop, args.start
        ):
            if args.verbose:
                print(f'Trying: {combination}')

            if (correct_password := give_a_try(args.file, combination)):
                print(f'Password found: {correct_password}')
                break

    else:
        give_a_try_worker.file = args.file

        with Pool(processes=args.processes) as pool:
            for correct_password in pool.imap_unordered(
                give_a_try_worker,
                generate_combinations(args.alphabet, args.stop, args.start),
                100
            ):
                if correct_password:
                    print(f'Password found: {correct_password}')
                    break

            pool.terminate()

    print(f'Time: {time() - start_time}')
