#############################
# Common Minecraft Launcher #
# Logger module,part of CMCL#
# copyright PuqiAR@2024     #
#############################
from logging import DEBUG,INFO,getLogger,StreamHandler
from colorlog import ColoredFormatter
from CMCL.DevConf import CMCL_DEV_MODE
LOGGER_NAME = "CMCL"

def get_logger(level=DEBUG):
    # 创建logger对象
    logger = getLogger(LOGGER_NAME)
    logger.setLevel(level)
    # 创建控制台日志处理器
    console_handler = StreamHandler()
    console_handler.setLevel(level)
    # 定义颜色输出格式
    color_formatter = ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s][%(module)s %(funcName)s%(threadName)s]%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    )
    # 将颜色输出格式添加到控制台日志处理器
    console_handler.setFormatter(color_formatter)
    # 移除默认的handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # 将控制台日志处理器添加到logger对象
    logger.addHandler(console_handler)
    return logger
logger = get_logger(DEBUG if CMCL_DEV_MODE else INFO)