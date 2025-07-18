import logging

import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudPreprocessor:
    def __init__(
        self,
        voxel_size: float = 0.05,
        normal_radius: float = 0.1,
        normal_max_nn: int = 30,
    ):
        self.voxel_size = voxel_size
        self.normal_radius = normal_radius
        self.normal_max_nn = normal_max_nn

    def run(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        pcd = self.downsample(pcd)
        pcd = self.estimate_normals(pcd)
        return pcd

    def downsample(
        self,
        pcd: o3d.geometry.PointCloud,
        voxel_size: float = None,
    ) -> o3d.geometry.PointCloud:
        voxel_size = self.voxel_size if voxel_size is None else voxel_size
        return pcd.voxel_down_sample(voxel_size)

    def estimate_normals(
        self,
        pcd: o3d.geometry.PointCloud,
        radius: float = None,
        max_nn: int = None,
    ) -> o3d.geometry.PointCloud:
        radius = self.normal_radius if radius is None else radius
        max_nn = self.normal_max_nn if max_nn is None else max_nn
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=radius,
                max_nn=max_nn,
            )
        )
        return pcd
