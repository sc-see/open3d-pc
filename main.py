import logging

import matplotlib.pyplot as plt

from src.open3d_pc.logging_config import setup_logging
from src.open3d_pc.point_cloud_loader import PointCloudLoader

logger = logging.getLogger(__name__)


def main():
    setup_logging(logging.INFO)
    
    loader = PointCloudLoader()
    pcd = loader.load()
    logger.info(f"Loaded point cloud with {len(pcd.points)} points.")

if __name__ == "__main__":
    main()
