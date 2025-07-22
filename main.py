import logging

import hydra
from omegaconf import DictConfig

from src.open3d_pc.logging_config import setup_logging
from src.open3d_pc.point_cloud_pipeline import PointCloudPipeline

logger = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    """
    Example entry point to run the point cloud processing pipeline with configuration.
    """
    setup_logging()

    pipeline = PointCloudPipeline.from_config(cfg)
    pcd, labels = pipeline.run()


if __name__ == "__main__":
    main()
