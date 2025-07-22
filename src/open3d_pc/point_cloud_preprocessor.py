import logging

import open3d as o3d

logger = logging.getLogger(__name__)


class PointCloudPreprocessor:
    """
    Preprocesses point clouds by downsampling and estimating surface normals.

    Attributes:
        voxel_size (float): Voxel size for downsampling. Defaults to 0.05.
        normal_radius (float): Radius for normal estimation. Defaults to 0.1.
        normal_max_nn (int): Maximum number of nearest neighbors for normal estimation.
            Defaults to 30.
    """

    def __init__(
        self,
        voxel_size: float = 0.05,
        normal_radius: float = 0.1,
        normal_max_nn: int = 30,
    ):
        self.voxel_size = voxel_size
        self.normal_radius = normal_radius
        self.normal_max_nn = normal_max_nn

    def preprocess(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Preprocess the point cloud by downsampling and estimating surface normals.

        Uses the instance's voxel size and normal estimation parameters.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud to preprocess.

        Returns:
            pcd (o3d.geometry.PointCloud): The preprocessed point cloud with
                downsampling and normals estimated.
        """
        pcd = self.downsample(pcd)
        pcd = self.estimate_normals(pcd)

        logger.info(f"Processed point cloud with {len(pcd.points)} points.")
        return pcd

    def downsample(
        self,
        pcd: o3d.geometry.PointCloud,
        voxel_size: float = None,
    ) -> o3d.geometry.PointCloud:
        """
        Downsample the point cloud using voxel downsampling.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud to downsample.
            voxel_size (float | None): Override the voxel size for downsampling. If
                None, uses the instance's `voxel_size`.

        Returns:
            down_pcd (o3d.geometry.PointCloud): The downsampled point cloud.
        
        Raises:
            ValueError: If voxel size is not positive.
        """
        voxel_size = self.voxel_size if voxel_size is None else voxel_size
        if voxel_size <= 0:
            raise ValueError(f"voxel_size must be positive, got {voxel_size}")
        
        down_pcd = pcd.voxel_down_sample(voxel_size)
        logger.debug(
            f"Downsampled point cloud from {len(pcd.points)} "
            f"to {len(down_pcd.points)} points."
        )

        return down_pcd

    def estimate_normals(
        self,
        pcd: o3d.geometry.PointCloud,
        radius: float = None,
        max_nn: int = None,
    ) -> o3d.geometry.PointCloud:
        """
        Estimate surface normals for the point cloud.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud for normal estimation.
            radius (float | None): Search radius for neighbors. If None, uses the
                instance's `normal_radius`.
            max_nn (int | None): Maximum number of nearest neighbors for normal
                estimation. If None, uses the instance's `normal_max_nn`.
        
        Returns:
            o3d.geometry.PointCloud: The point cloud with estimated normals.
        
        Raises:
            ValueError: If radius or max_nn is not positive.
        """
        radius = self.normal_radius if radius is None else radius
        max_nn = self.normal_max_nn if max_nn is None else max_nn
        if radius <= 0:
            raise ValueError(f"radius must be positive, got {radius}")
        if max_nn <= 0:
            raise ValueError(f"max_nn must be positive, got {max_nn}")
        
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=radius,
                max_nn=max_nn,
            )
        )

        return pcd
