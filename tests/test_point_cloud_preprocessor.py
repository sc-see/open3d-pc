import numpy as np
import open3d as o3d
import pytest

from src.open3d_pc.point_cloud_preprocessor import PointCloudPreprocessor


def test_downsample_reduces_points(synthetic_pcd):
    preprocesser = PointCloudPreprocessor()
    downsampled_pcd = preprocesser.downsample(synthetic_pcd)
    
    assert isinstance(downsampled_pcd, o3d.geometry.PointCloud)
    assert len(downsampled_pcd.points) < len(synthetic_pcd.points)


def test_downsample_invalid_voxel_size(synthetic_pcd):
    preprocesser = PointCloudPreprocessor()
    
    with pytest.raises(ValueError, match="voxel_size must be positive"):
        preprocesser.downsample(synthetic_pcd, voxel_size=0.0)


def test_estimate_normals_add_normals(synthetic_pcd):
    preprocesser = PointCloudPreprocessor()
    pcd_with_normals = preprocesser.estimate_normals(synthetic_pcd)
    
    assert isinstance(pcd_with_normals, o3d.geometry.PointCloud)
    assert pcd_with_normals.has_normals()
    
    normals = np.asarray(pcd_with_normals.normals)
    assert normals.shape == (len(pcd_with_normals.points), 3)

def test_preprocess(synthetic_pcd):
    preprocesser = PointCloudPreprocessor()
    preprocessed_pcd = preprocesser.preprocess(synthetic_pcd)
    
    assert isinstance(preprocessed_pcd, o3d.geometry.PointCloud)
    assert len(preprocessed_pcd.points) < len(synthetic_pcd.points)
    assert preprocessed_pcd.has_normals()
