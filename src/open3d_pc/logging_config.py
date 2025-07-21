import logging
import logging.config
import yaml

from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging(cfg_path="conf/logging.yaml", default_level=logging.INFO):
    """
    Set up basic logging configuration from YAML file.
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    try:
        with open(cfg_path, "rt", encoding="utf-8") as _f:
            log_config = yaml.safe_load(_f)
        logging.config.dictConfig(log_config)

    except Exception as e:
        logger.error(f"Error loading logging config: {e}")
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.info("Basic config is being used.")
