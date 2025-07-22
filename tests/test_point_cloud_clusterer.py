from pathlib import Path

import numpy as np
import open3d as o3d

from src.open3d_pc.point_cloud_clusterer import PointCloudClusterer


def test_cluster_multiple_clusters(synthetic_clustered_pcd):
    clusterer = PointCloudClusterer()
    
    labels, clustered_pcd = clusterer.cluster(synthetic_clustered_pcd)
    assert isinstance(labels, np.ndarray)
    assert len(labels) == len(synthetic_clustered_pcd.points)
    assert (labels >= -1).all()
    assert len(np.unique(labels)) == 3


def test_colorize_clusters(synthetic_clustered_pcd):
    clusterer = PointCloudClusterer()
    labels, clustered_pcd = clusterer.cluster(synthetic_clustered_pcd)

    clusterer._colorize_clusters(clustered_pcd, labels, labels.max() + 1)

    assert isinstance(clustered_pcd, o3d.geometry.PointCloud)
    assert clustered_pcd.has_colors()
    
    colors = np.asarray(clustered_pcd.colors)
    assert not np.all(colors == 0)
    assert colors.shape == (len(synthetic_clustered_pcd.points), 3)

    # Check number of unique colors matches number of clusters
    unique_colors = np.unique(colors[labels >= 0], axis=0)
    assert len(unique_colors) == labels.max() + 1


def test_save_clusters(synthetic_clustered_pcd, tmp_path):
    clusterer = PointCloudClusterer()
    output_dir = tmp_path / "clusters"
    labels, clustered_pcd = clusterer.cluster(
        synthetic_clustered_pcd,
        save_clusters=True,
        output_dir=output_dir,
    )

    output_files = list(output_dir.glob("cluster_*.ply"))
    assert len(output_files) == labels.max() + 1

    for file in output_files:
        assert file.is_file()
        assert file.stat().st_size > 0
