import numpy as np
import open3d as o3d

from src.open3d_pc.point_cloud_clusterer import PointCloudClusterer


def test_cluster_multiple_clusters():
    clusterer = PointCloudClusterer()
    
    points = np.random.rand(100, 3)
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    
    labels, clustered_pcd = clusterer.cluster(pcd)
    assert isinstance(labels, np.ndarray)
    assert isinstance(clustered_pcd, o3d.geometry.PointCloud)
    
    assert labels.shape[0] > 1
