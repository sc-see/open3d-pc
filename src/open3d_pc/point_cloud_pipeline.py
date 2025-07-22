import logging

import numpy as np
import open3d as o3d
from omegaconf import DictConfig, OmegaConf

from src.open3d_pc.point_cloud_loader import PointCloudLoader
from src.open3d_pc.point_cloud_preprocessor import PointCloudPreprocessor
from src.open3d_pc.point_cloud_clusterer import PointCloudClusterer

logger = logging.getLogger(__name__)


class PointCloudPipeline:
    """
    Pipeline for loading, preprocessing, and clustering point cloud data.

    This class composes the following components:
        - PointCloudLoader for loading point cloud data.
        - PointCloudPreprocessor for downsampling and normal estimation.
        - PointCloudClusterer for clustering the point cloud data.
    
    Configuration for each component can be provided via dictionaries or DictConfig 
    objects and are passed to the respective classes during initialisation.

    Attributes:
        loader (PointCloudLoader): Loader instance configured with loader_cfg.
        preprocessor (PointCloudPreprocessor): Preprocessor instance configured with 
            preprocessor_cfg.
        clusterer (PointCloudClusterer): Clusterer instance configured with 
            clusterer_cfg.
        cluster_output_cfg (dict): Dictionary for cluster output, including options for
            visualisation and saving clusters.
    """

    def __init__(
        self,
        loader_cfg: dict,
        preprocessor_cfg: dict,
        clusterer_cfg: dict,
        cluster_output_cfg: dict,
    ):
        """
        Initialise the PointCloudPipeline with separate config dictionaries.

        Args:
            loader_cfg (dict): Configuration for PointCloudLoader.
            preprocessor_cfg (dict): Configuration for PointCloudPreprocessor.
            clusterer_cfg (dict): Configuration for PointCloudClusterer.
            cluster_output_cfg (dict): Configuration for cluster output options, such as
                "visualize", "save_clusters", and "output_dir".
        """
        self.loader = PointCloudLoader(loader_cfg.get("path"))
        self.preprocessor = PointCloudPreprocessor(**preprocessor_cfg)
        self.clusterer = PointCloudClusterer(**clusterer_cfg)
        self.cluster_output_cfg = cluster_output_cfg

    @classmethod
    def from_config(cls, cfg: DictConfig | dict) -> "PointCloudPipeline":
        """
        Alternative constrcutor to create a PointCloudPipeline instance from a
        DictConfig or a nested config dictionary.

        Args:
            cfg (DictConfig | dict): Configuration DictConfig object or dictionary
                containing keys for "loader", "preprocessor", "clusterer", and
                "cluster_output".
        
        Returns:
            PointCloudPipeline: Instance of PointCloudPipeline with configs applied.
        """
        if isinstance(cfg, DictConfig):
            cfg = OmegaConf.to_container(cfg, resolve=True)
        
        return cls(
            loader_cfg=cfg.get("loader", {}),
            preprocessor_cfg=cfg.get("preprocessor", {}),
            clusterer_cfg=cfg.get("clusterer", {}),
            cluster_output_cfg=cfg.get("cluster_output", {}),
        )

    def run(self) -> tuple[o3d.geometry.PointCloud, np.ndarray]:
        """
        Execute the full point cloud processing pipeline: load, preprocess, and cluster.

        Returns:
            tuple[o3d.geometry.PointCloud, np.ndarray]: A tuple containing:
                - clustered_pcd (o3d.geometry.PointCloud): The processed point cloud
                  after clustering, with optional colours applied.
                - labels (np.ndarray): Cluster labels for each point in the point cloud.
        """
        logger.info("Running point cloud pipeline.")
        pcd = self.loader.load()
        processed_pcd = self.preprocessor.preprocess(pcd)
        labels, clustered_pcd = self.clusterer.cluster(
            processed_pcd,
            visualize=self.cluster_output_cfg.get("visualize", False),
            save_clusters=self.cluster_output_cfg.get("save_clusters", False),
            output_dir=self.cluster_output_cfg.get("output_dir", "output_clusters"),
        )
        logger.info("Point cloud pipeline completed.")

        return clustered_pcd, labels
