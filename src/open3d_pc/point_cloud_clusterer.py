import logging
from pathlib import Path

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
        visualize: bool = False,
        save_clusters: bool = False,
        output_dir: str | Path = "clusters",
    ) -> tuple[np.ndarray, o3d.geometry.PointCloud]:
        labels = pcd.cluster_dbscan(eps=self.eps, min_points=self.min_points)
        labels = np.array(labels)
        
        valid_mask = labels >= 0
        if valid_mask.any():
            valid_labels = labels[valid_mask]
            n_clusters = valid_labels.max() + 1
        else:
            logger.info(
                f"No clusters found with {self.eps=} and {self.min_points}."
            )
            return labels, pcd

        if visualize:
            colors = np.zeros((len(labels), 3))
            hue_values = np.linspace(0, 1, n_clusters + 1)[:-1]
            cluster_colors = plt.cm.hsv(hue_values)[:, :3]

            colors[valid_mask] = cluster_colors[valid_labels]
            pcd.colors = o3d.utility.Vector3dVector(colors)

            o3d.visualization.draw_geometries([pcd])

        if save_clusters:
            output_dir = Path(output_dir).resolve()
            output_dir.mkdir(parents=True, exist_ok=True)

            for cluster_id in range(n_clusters):
                indices = np.where(labels == cluster_id)[0]
                cluster_pcd = pcd.select_by_index(indices)
                cluster_path = output_dir / f"cluster_{cluster_id}.ply"
                o3d.io.write_point_cloud(str(cluster_path), cluster_pcd)
            logger.info(
                f"Saved {n_clusters} clusters to {output_dir}."
            )

        logger.info(f"Clustered point cloud into {labels.max() + 1} clusters.")

        return labels, pcd
