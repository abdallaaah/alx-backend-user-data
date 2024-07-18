#!/user/bin/env python3
""""auth function """
import bcrypt


def _hash_password(self, password: str):
    """return hasehd password from the saulted password
    utf-8 password -> salted (random text added to password)
    -> hash the salt
    """
    if password:
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash
