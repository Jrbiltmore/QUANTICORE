
from flask_limiter import Limiter
limiter = Limiter(key_func=get_remote_address)
