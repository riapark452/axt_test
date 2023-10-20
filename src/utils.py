import random
import string

ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))

# def setup_logger(folder_path: str = "../logs", camera_ip: str = "ip_address", max_size_in_mb: int = 10):
#     # create log folder if not exists
#     create_dir(folder_path)
#
#     filename = folder_path + '/' + camera_ip + ".log"
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     logFormatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] - %(message)s")
#
#     ch = logging.StreamHandler(sys.stdout)
#     ch.setFormatter(logFormatter)
#     logger.addHandler(ch)
#
#     fh = handlers.RotatingFileHandler(filename, mode='a', maxBytes=(1048576 * max_size_in_mb), backupCount=5)
#     fh.setFormatter(logFormatter)
#     logger.addHandler(fh)
#
#     return logger
#
# LOGGER = setup_logger()
