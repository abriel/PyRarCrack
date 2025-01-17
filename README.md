# PyRarCrack
Bruteforce attack for .rar using unrar

```
usage: pyrarcrack.py [-h] [--start START] [--stop STOP] [--verbose VERBOSE]
                     [--alphabet ALPHABET] [--file FILE]

Python combination generator to unrar

optional arguments:
  -h, --help           show this help message and exit
  --start START        Number of characters of the initial string [1 -> "a", 2-> "aa"]
  --stop STOP          Number of characters of the final string [3 -> "ßßß"]
  --verbose VERBOSE    Show combintations
  --alphabet ALPHABET  alternative chars to combinations
  --advanced-alphabet ADVANCED_ALPHABET
                        a file contains the own alphabet for a password char (per a line)
  --file FILE          .rar file [file.rar]
  --processes PROCESSES
                        number of workers
  --no-mt               do not use multiprocessing
```

## Performance notes

#### Implementations

There are multiple implementations. Depends on python module availability,
corresponding method to be used:

* unrardll. Shows as most efficient, but the same time the hardest to install.
Doing compilation during the installation. 
Requires /usr/lib/libunrar.so and /usr/include/unrar/dll.hpp (libunrar package).  
With arguments `--start 3 --stop 3 --alphabet 0987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ` on i7-8565U takes 
```
real  0m10.652s
user  0m9.424s
sys 0m1.178s
```

* unrar. Second by efficiency method. Does not compile anything during installation.
Loads /usr/lib/libunrar.so dynamically in runtime.  
With arguments `--start 3 --stop 3 --alphabet 0987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ` on i7-8565U takes 
```
real  0m19.029s
user  0m15.776s
sys 0m3.174s
```

* subprocess. Fallback method. Calling unrar binary in subshell process.  
With arguments `--start 3 --stop 3 --alphabet 0987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ` on i7-8565U takes 
```
real  3m56.164s
user  2m58.832s
sys 1m14.105s
```

Note: It is on you to install unrardll or unrar modules.

#### RAR versions

Noticed that newer archive format has more stronger encryption which affects on bruteforce time.
```
$ unrar l /var/tmp/test.rar 

UNRAR 6.22 freeware      Copyright (c) 1993-2023 Alexander Roshal

Archive: /var/tmp/test.rar
Details: RAR 5
_________^^^^^^_______
```

using the same `--start 3 --stop 3 --alphabet 0987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ` on i7-8565U

|RAR format \ method       | unrardll  | unrar |
|--------------------------|-----------|-------|
|RAR 5                     | 14m49s    | 16m3s |
|RAR 4                     | 10s       | 20s   |


#### Multiprocessing 

You still have ability to run with origin algorithm by providing `--no-mt` argument.

By default number of processes equals to number of CPU cores minus 1.  
You can specify the number by providing an `--processes NN` argument.

Timing measurements with `--start 3 --stop 3 --alphabet 0987654321ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef`

| engine \ no. processes | --no-mt |  1  | 2  | 3  | 4  |
|------------------------|---------|-----|----|----|----|
|  unrardll              | 17.0s   |17.3s|8.6s|5.9s|5.2s|

## Advanced alphabet

If you know precise length of a password and character variants per a char position, you
can use `--advanced-alphabet` by providing a file contains those variants. Each line of that file
should contain an alphabet for a particular letter of a password. Where line number represents
a letter position.

## Example

```
$ python pyrarcrack.py --start 10 --stop 10 --file example_path.rar --alphabet 1234567890
Loaded engine: unrardll

Password found: 1234567890
Time: 0.06715750694274902
```
