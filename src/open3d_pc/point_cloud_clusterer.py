import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudClusterer:
    """
    Clusters a point cloud using the DBSCAN algorithm.

    Attributes:
        eps (float): Maximum distance between two points to be considered neighbors.
            Defaults to 0.108.
        min_points (int): Minimum number of points required to form a cluster.
            Defaults to 20.
    """

    def __init__(self, eps: float = 0.108, min_points: int = 20):
        self.eps = eps
        self.min_points = min_points

    def cluster(
        self,
        pcd: o3d.geometry.PointCloud,
        visualize: bool = False,
        save_clusters: bool = False,
        output_dir: str | Path = "clusters",
    ) -> tuple[np.ndarray, o3d.geometry.PointCloud]:
        """
        Cluster the point cloud using DBSCAN. Optionally visualise the clusters or save
        the clusters to files.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud to cluster.
            visualize (bool): Whether to colour and display the clusters. Defaults to
                False.
            save_clusters (bool): Whether to save each cluster to disk. Defaults to
                False.
            output_dir (str | Path): Directory to save the clusters if `save_clusters`
                is True. Defaults to "clusters".

        Returns:
            tuple[np.ndarray, o3d.geometry.PointCloud]: A tuple containing:
                - labels (np.ndarray): Cluster labels for each point in the point cloud.
                - pcd (o3d.geometry.PointCloud): The point cloud with optional cluster
                  colours applied.
        """
        labels = pcd.cluster_dbscan(eps=self.eps, min_points=self.min_points)
        labels = np.array(labels)

        if not (labels >= 0).any():
            logger.info(
                f"No clusters found with eps={self.eps}, min_points={self.min_points}."
            )
            return labels, pcd

        n_clusters = labels.max() + 1
        logger.info(f"Clustered point cloud into {labels.max() + 1} clusters.")

        if visualize:
            self._colorize_clusters(pcd, labels, n_clusters)
            o3d.visualization.draw_geometries([pcd])

        if save_clusters:
            self._save_clusters(pcd, labels, n_clusters, output_dir)

        return labels, pcd

    def _colorize_clusters(
        self,
        pcd: o3d.geometry.PointCloud,
        labels: np.ndarray,
        n_clusters: int,
    ) -> None:
        """
        Apply unique colours to each cluster in the point cloud for visualisation.

        Args:
            pcd (o3d.geometry.PointCloud): The point cloud to modify.
            labels (np.ndarray): Array of cluster labels for each point.
            n_clusters (int): Number of clusters found in the point cloud.

        Returns:
            None
        """
        valid_mask = labels >= 0
        valid_labels = labels[valid_mask]

        colors = np.zeros((len(labels), 3))
        hue_values = np.linspace(0, 1, n_clusters + 1)[:-1]
        cluster_colors = plt.cm.hsv(hue_values)[:, :3]

        colors[valid_mask] = cluster_colors[valid_labels]
        pcd.colors = o3d.utility.Vector3dVector(colors)

    def _save_clusters(
        self,
        pcd: o3d.geometry.PointCloud,
        labels: np.ndarray,
        n_clusters: int,
        output_dir: str | Path,
    ) -> None:
        """
        Save each cluster from the point cloud as separate PLY files.

        Args:
            pcd (o3d.geometry.PointCloud): The point cloud containing the clusters.
            labels (np.ndarray): Array of cluster labels for each point.
            n_clusters (int): Number of clusters found in the point cloud.
            output_dir (str | Path): Directory to save the cluster files.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for cluster_id in range(n_clusters):
            indices = np.where(labels == cluster_id)[0]
            cluster_pcd = pcd.select_by_index(indices)
            cluster_path = output_dir / f"cluster_{cluster_id}.ply"
            o3d.io.write_point_cloud(str(cluster_path), cluster_pcd)
        logger.info(
            f"Saved {n_clusters} clusters to {output_dir}."
        )
