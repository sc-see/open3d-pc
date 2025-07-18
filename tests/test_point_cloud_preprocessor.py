import numpy as np
import open3d as o3d

from src.open3d_pc.point_cloud_preprocessor import PointCloudPreprocessor


def test_downsample():
    preprocesser = PointCloudPreprocessor()
    points = np.random.rand(100, 3)
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    downsampled_pcd = preprocesser.downsample(pcd)
    assert len(downsampled_pcd.points) < len(pcd.points)
