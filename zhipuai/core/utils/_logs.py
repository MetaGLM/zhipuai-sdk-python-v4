import os
import logging

logger: logging.Logger = logging.getLogger("zhipuai")
httpx_logger: logging.Logger = logging.getLogger("httpx")


def _basic_config() -> None:
    # e.g.  2021-07-01 12:34:56 - zhipuai:123 - INFO] message
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup_logging() -> None:
    env = os.environ.get("ZHIPUAI_LOG")
    if env == "debug":
        _basic_config()
        logger.setLevel(logging.DEBUG)
        httpx_logger.setLevel(logging.DEBUG)
    elif env == "info":
        _basic_config()
        logger.setLevel(logging.INFO)
        httpx_logger.setLevel(logging.INFO)
