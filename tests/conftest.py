import numpy as np
import open3d as o3d
import pytest


@pytest.fixture
def synthetic_pcd():
    points = np.random.rand(500, 3)
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

    return pcd

@pytest.fixture
def synthetic_clustered_pcd():
    # Create 3 clusters in 3D space
    cluster1 = np.random.randn(50, 3) * 0.02 + np.array([0, 0, 0])
    cluster2 = np.random.randn(50, 3) * 0.02 + np.array([0.5, 0.5, 0.5])
    cluster3 = np.random.randn(50, 3) * 0.02 + np.array([1, 1, 1])
    all_points = np.vstack([cluster1, cluster2, cluster3])

    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(all_points))

    return pcd
