import logging
import os

import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudLoader:
    def __init__(self, path: str | None = None):
        self.path = path
        self.pcd = None

    def load(self):
        if self.path is None:
            logger.info("No path provided, using default Eagle Point Cloud dataset.")
            data = o3d.data.EaglePointCloud()
            self.path = data.path
        
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Point cloud file not found: {self.path}")
        if not self.path.lower().endswith(('.pcd', '.ply', '.xyz', '.pts')):
            raise ValueError(f"Unsupported file format: {self.path}")
        
        self.pcd = o3d.io.read_point_cloud(self.path)
        logger.info(f"Loaded point cloud with {len(self.pcd.points)} points.")

        return self.pcd
