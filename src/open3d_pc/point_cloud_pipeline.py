import logging

import numpy as np
import open3d as o3d
from omegaconf import DictConfig

from src.open3d_pc.point_cloud_loader import PointCloudLoader
from src.open3d_pc.point_cloud_preprocessor import PointCloudPreprocessor
from src.open3d_pc.point_cloud_clusterer import PointCloudClusterer

logger = logging.getLogger(__name__)


class PointCloudPipeline:
    def __init__(
        self,
        loader_cfg: DictConfig,
        preprocessor_cfg: DictConfig,
        clusterer_cfg: DictConfig,
        cluster_output_cfg: DictConfig,
    ):
        self.loader = PointCloudLoader(loader_cfg.path)
        self.preprocessor = PointCloudPreprocessor(**preprocessor_cfg)
        self.clusterer = PointCloudClusterer(**clusterer_cfg)
        self.cluster_output_cfg = cluster_output_cfg

    def run(self) -> tuple[o3d.geometry.PointCloud, np.ndarray]:
        logger.info("Running point cloud pipeline.")
        pcd = self.loader.load()
        processed_pcd = self.preprocessor.preprocess(pcd)
        labels, clustered_pcd = self.clusterer.cluster(
            processed_pcd,
            visualize=self.cluster_output_cfg.visualize,
            save_clusters=self.cluster_output_cfg.save_clusters,
            output_dir=self.cluster_output_cfg.output_dir,
        )
        logger.info("Point cloud pipeline completed.")

        return clustered_pcd, labels
