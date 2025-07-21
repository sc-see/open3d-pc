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
    
    preprocessor = PointCloudPreprocessor(**cfg.preprocessor)
    processed_pcd = preprocessor.run(pcd)

    clusterer = PointCloudClusterer(**cfg.clusterer)
    labels, clustered_pcd = clusterer.cluster(processed_pcd)

    o3d.visualization.draw_geometries([clustered_pcd])


if __name__ == "__main__":
    main()
