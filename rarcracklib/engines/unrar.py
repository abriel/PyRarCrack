from unrar import rarfile

def give_a_try(file_path, password):
    '''
    Testing a password using unrar API from libunrar. Another python wrapper
    Requires /usr/lib/libunrar.so (libunrar)
    But distributed as pre-build python module - less pain on install comparing to unrardll
    '''
    rar_file = rarfile.RarFile(file_path)

    rar_file.setpassword(password)

    if rar_file.testrar():
        return None

    return password

give_a_try.engine_name = 'unrar'
