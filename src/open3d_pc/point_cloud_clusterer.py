import logging

import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudClusterer:
    def __init__(self, eps: float = 0.108, min_points: int = 20):
        self.eps = eps
        self.min_points = min_points

    def cluster(
        self,
        pcd: o3d.geometry.PointCloud,
    ) -> tuple[np.ndarray, o3d.geometry.PointCloud]:
        labels = pcd.cluster_dbscan(eps=self.eps, min_points=self.min_points)
        labels = np.array(labels)
        
        # Assign colors based on cluster labels
        colors = np.zeros((len(labels), 3))
        valid_mask = labels >= 0
        if valid_mask.any():
            valid_labels = labels[valid_mask]
            n_clusters = valid_labels.max() + 1

            hue_values = np.linspace(0, 1, n_clusters + 1)[:-1]
            cluster_colors = plt.cm.hsv(hue_values)[:, :3]

            colors[valid_mask] = cluster_colors[valid_labels]

        pcd.colors = o3d.utility.Vector3dVector(colors)
        logger.info(f"Clustered point cloud into {labels.max() + 1} clusters.")

        return labels, pcd
