import logging
import os

import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudLoader:
    """
    Loads point cloud data from a given file path or a default sample dataset.

    If no path is provided, the loader defaults to the Eagle Point Cloud sample dataset
    from Open3D.

    Attributes:
        path (str | None): Path to the point cloud file. Defaults to None.
        pcd (o3d.geometry.PointCloud | None): The loaded point cloud object after
            calling `load()`.
    """

    def __init__(self, path: str | None = None):
        self.path = path
        self.pcd = None

    def load(self):
        """
        Load the point cloud from the specified path or the default dataset.

        Returns:
            self.pcd (o3d.geometry.PointCloud): The loaded point cloud object.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is unsupported.
        """
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
