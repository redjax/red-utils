RED_UTILS_FMT: str = (
    "[%(asctime)s] [%(levelname)s] [(red_utils).%(module)s:%(lineno)d > %(funcName)s()]: %(message)s"
)
RED_UTILS_DETAIL_FMT: str = (
    "[%(asctime)s] [%(levelname)s] [(red_utils).%(module)s] [path:%(pathname)s:%(lineno)d] [method:%(funcName)s()]: %(message)s"
)

MESSAGE_FMT_STANDARD: str = str(
    "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d > %(funcName)s()]: %(message)s"
)
MESSAGE_FMT_DETAILED: str = (
    "[%(asctime)s] [%(levelname)s] [module:%(module)s] [path:%(pathname)s:%(lineno)d] [method:%(funcName)s()]: %(message)s"
)
DATE_FMT_STANDARD: str = "%Y-%m-%d %H:%M:%S"
