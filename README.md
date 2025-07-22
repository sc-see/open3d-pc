# Point Cloud Processing using Open3D

This project performs 3D point cloud processing using Open3D. The current functionalities include common preprocessing steps done on point cloud data, including **downsampling**, **surface normals estimation**, and **clustering**.

## Project Structure

### Folder Structure

- `conf/`: Configuration files to manage paramters for the pipeline
- `src/open3d_pc/`: Source code modules implementing loader, preprocessor, and clusterer classes
- `tests/`: Unit tests for core modules
- `main.py`: Entry point to run the pipeline
- `conda.yaml`, `pyproject.toml`, `pixi.lock`: Environment and dependency management files

```shell
.
├── conf
│   ├── config.yaml
│   └── logging.yaml
├── src
│   └── open3d_pc
│       ├── point_cloud_clusterer.py
│       ├── point_cloud_loader.py
│       ├── point_cloud_pipeline.py
│       └── point_cloud_preprocessor.py
├── tests
│   ├── conftest.py
│   ├── test_point_cloud_clusterer.py
│   ├── test_point_cloud_loader.py
│   └── test_point_cloud_preprocessor.py
├── conda.yaml
├── main.py
├── pixi.lock
├── pyproject.toml
└── README.md
```

### Code Architecture

This project adopts OOP principles, using separate classes to implement each core point cloud processing step. Additionally, a `PointCloudPipeline` class orchestrates these components, managing the overall workflow from loading to clustering.

| Functionality | Corresponding Class | Description |
| ------------- | ------------------- | ----------- |
| Orchestrating pipeline        | `PointCloudPipeline`      | Coordinates loading, preprocessing, and clustering    |
| Loading point clouds          | `PointCloudLoader`        | Loads point cloud files or a default sample           |
| Downsampling                  | `PointCloudPreprocessor`  | Downsamples point cloud to reduce point density       |
| Surface normals estimation    | `PointCloudPreprocessor`  | Estimates surface normals to capture surface geometry |
| Clustering                    | `PointCloudClusterer`     | Separates point cloud into clusters                   |

The diagram below shows the UML class diagram of the point cloud processing pipeline design.

![UML class diagram](docs/pointcloud_pipeline_class_diagram.drawio.png)
**Fig 1.** UML class diagram of the point cloud processing pipeline.

## Getting Started

### Clone the repository

```shell
git clone https://github.com/sc-see/open3d-pc.git
cd open3d-pc
```

### Set up the environment

**Option A**: Using [Pixi](https://pixi.sh/latest/)

```shell
pixi install
pixi run python main.py
```

**Option B**: Using Conda

```shell
conda env create -f conda.yaml
conda activate point-cloud-env
python main.py
```

This will run the full pipeline using the configuration provided in [`conf/config.yaml`](conf/config.yaml).

> 💡 **Tip:** `PointCloudPipeline` can also be imported and used directly in your own scripts.
>
> ```python
> from src.open3d_pc.pipeline import PointCloudPipeline
> 
> pipeline = PointCloudPipeline(...)
> pcd, labels = pipeline.run()
> ```

## Configuration

This project uses [Hydra](https://hydra.cc/) for configuration management. Parameters are defined in [`conf/config.yaml`](conf/config.yaml), which can be modified. Alternatively, parameters can also be overriden at runtime via the command line.

### Configuration Parameters

Below is an overview of the key configuration parameters:

| Parameter | Default | Description |
| --------- | ------- | ----------- |
| `loader.path`                     | *empty* (default Eagle dataset)   | Path to the point cloud file. If empty, loads the default Eagle Point Cloud sample dataset. |
| `preprocessor.voxel_size`         | `0.05`                            | Voxel size for downsampling point clouds. Smaller values preserve more detail but increase computation. |
| `preprocessor.normal_radius`      | `0.1`                             | Search radius for neighbouring points to estimate surface normals. Affects normal accuracy and smoothness. |
| `preprocessor.normal_max_nn`      | `30`                              | Maximum number of neighbouring points to use for normal estimation. |
| `clusterer.eps`                   | `0.108`                           | Maximum distance between two points to be considered neighbours in DBSCAN clustering. |
| `clusterer.min_points`            | `20`                              | Minimum number of points to form a cluster in DBSCAN. |
| `cluster_output.visualize`        | `true`                            | Whether to colorise and display clustered point clouds for visualisation. |
| `cluster_output.save_clusters`    | `false`                           | Whether to save each cluster as a separate PLY file. |
| `cluster_output.output_dir`       | `"clusters"`                      | Directory where clusters are saved if `save_clusters` is `true`. |

### Overriding from Command Line

Hydra allows users to override configuration parameters directly from the command line without modifying the YAML files, which can be useful for testing different settings or running parameter sweeps.

```
# Override single parameters
pixi run python main.py preprocessor.voxel_size=0.02 clusterer.min_points=10
```

Hydra also supports multi-run sweeps, which execute the script multiple times with different parameter combinations:

```
# Sweep over multiple voxel sizes
pixi run python main.py --multirun preprocessor.voxel_size=0.02,0.03,0.04

# Sweep over combinations of voxel size and min_points
pixi run python main.py --multirun preprocessor.voxel_size=0.02,0.03 clusterer.min_points=10,20
```

## Examples

This section showcases intermediate results generated by running the point cloud processing pipeline using the default configuration provided in this repository.

| Description | Render |
| ----------- | :----: |
| **Input Point Cloud**                    | ![Input](docs/examples/input.png)<br>*Raw input point cloud*                                   |
| **Downsampled Point Cloud**              | ![Downsampled](docs/examples/downsampled.png)<br>*After voxel downsampling*                    |
| **Normals (Arrows)**                     | ![Normals Arrows](docs/examples/normals_arrows.png)<br>*Normals as black arrows*               |
| **Normals (Colored by Direction)**       | ![Normals Colored](docs/examples/normals_colored.png)<br>*Points colored by normal direction*  |
| **Clustered (Colored)**                  | ![Clustered](docs/examples/clustered_colored.png)<br>*Clusters shown with distinct colors*     |

All images were rendered using consistent camera parameters to ensure a stable viewpoint across stages.
