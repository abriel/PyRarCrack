import unrardll

def give_a_try(file_path, password):
    '''
    Testing a password using unrar API from libunrar.
    Requires /usr/lib/libunrar.so (libunrar)
    and unrardll python package (python3-unrardll on ubuntu / debian, python-unrardll on ArchLinux
    '''
    try:
        unrardll.extract_member(file_path, lambda x: True, password)
    except unrardll.BadPassword:
        return None

    return password

give_a_try.engine_name = 'unrardll'
