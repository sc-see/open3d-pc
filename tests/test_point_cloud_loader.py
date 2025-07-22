import os

import open3d as o3d
import pytest

from src.open3d_pc.point_cloud_loader import PointCloudLoader


def test_load_valid_path(monkeypatch):
    synthetic_path = "/path/sample.ply"
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    monkeypatch.setattr(
        o3d.io,
        "read_point_cloud",
        lambda path: o3d.geometry.PointCloud(),
    )
    loader = PointCloudLoader(path=synthetic_path)
    pcd = loader.load()

    assert loader.path == synthetic_path
    assert isinstance(pcd, o3d.geometry.PointCloud)


def test_load_file_not_found(monkeypatch):
    synthetic_path = "/path/non_existent.ply"
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    loader = PointCloudLoader(path=synthetic_path)

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_unsupported_format(monkeypatch):
    synthetic_path = "/path/sample.txt"
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    loader = PointCloudLoader(path=synthetic_path)

    with pytest.raises(ValueError):
        loader.load()
