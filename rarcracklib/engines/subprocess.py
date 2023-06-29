from subprocess import Popen, PIPE

special_chars = "();<>`|~\"&\'}]"

def give_a_try(file_path, password):
    '''
    Testing a password using a call to subshell to unrar binary.
    Less efficient method.
    '''
    cmd = Popen(
        f'unrar t -p{escape_shell(password)} {file_path}'.split(),
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = cmd.communicate()

    if 'All OK' in out.decode():
        return password

def escape_shell(string):
    """Format chars to write them in shell."""
    formated = map(
        lambda char: char if char not in special_chars else f'\\{char}', string
    )
    return ''.join(formated)

give_a_try.engine_name = 'subprocess'
