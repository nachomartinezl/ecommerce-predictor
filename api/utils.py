import hashlib
import os

def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

def allowed_name(name):
    """
    Checks if the format for the text for the name received is acceptable

    Parameters
    ----------
    name : str
        
    Returns
    -------
    bool
        True if the string has allowed extension
    """
    return len(name) > 10

def allowed_description(description):
    """
    Checks if the format for the text for the description received is acceptable

    Parameters
    ----------
    name : str
        
    Returns
    -------
    bool
        True if the string has allowed extension
    """
    return 20 < len(description) < 400


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Current implementation will return the original file name.
    # TODO
    new_name = hashlib.md5(file.read()).hexdigest()
    file.seek(0)
    return f'{new_name}{os.path.splitext(file.filename)[1]}'
