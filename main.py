import logging

import hydra
import open3d as o3d
from omegaconf import DictConfig

from src.open3d_pc.logging_config import setup_logging
from src.open3d_pc.point_cloud_pipeline import PointCloudPipeline

logger = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    setup_logging()
    
    pipeline = PointCloudPipeline(
        loader_cfg=cfg.loader,
        preprocessor_cfg=cfg.preprocessor,
        clusterer_cfg=cfg.clusterer
    )
    pcd, _ = pipeline.run()

    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    main()
