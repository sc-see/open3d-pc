import logging

import hydra
import matplotlib.pyplot as plt
import open3d as o3d
from omegaconf import DictConfig

from src.open3d_pc.logging_config import setup_logging
from src.open3d_pc.point_cloud_loader import PointCloudLoader
from src.open3d_pc.point_cloud_preprocessor import PointCloudPreprocessor
from src.open3d_pc.point_cloud_clusterer import PointCloudClusterer

logger = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    setup_logging()
    
    loader = PointCloudLoader(cfg.loader.path)
    pcd = loader.load()
    logger.info(f"Loaded point cloud with {len(pcd.points)} points.")
    
    preprocessor = PointCloudPreprocessor(**cfg.preprocessor)
    processed_pcd = preprocessor.run(pcd)
    logger.info(f"Processed point cloud with {len(processed_pcd.points)} points.")

    clusterer = PointCloudClusterer(**cfg.clusterer)
    labels, clustered_pcd = clusterer.cluster(processed_pcd)
    logger.info(f"Clustered point cloud into {labels.max() + 1} clusters.")

    o3d.visualization.draw_geometries([clustered_pcd])


if __name__ == "__main__":
    main()
