import unrardll

def give_a_try(file_path, password, fname=None):
    '''
    Testing a password using unrar API from libunrar.
    Requires /usr/lib/libunrar.so (libunrar)
    and unrardll python package (python3-unrardll on ubuntu / debian, python-unrardll on ArchLinux
    '''
    if fname:
        filename_selector = lambda x: x['filename'] == fname
    else:
        filename_selector = lambda x: True

    try:
        unrardll.extract_member(file_path, filename_selector, password)
    except unrardll.BadPassword:
        return None
    except unrardll.unrar.UNRARError as e:
        if e.args[0] == 'ERAR_BAD_PASSWORD':
            return None

        raise

    if fname:
        return password

    if all((give_a_try(file_path, password, x) for x in unrardll.names(file_path))):
        return password

give_a_try.engine_name = 'unrardll'
