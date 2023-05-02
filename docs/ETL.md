# Extract - Transform - Load (ETL) Pipeline

Steps through key design decisions and statistics around our ETL pipeline for handling raw trajectory data (stored as
timestamped directories with a top-level `trajectory.h5` and subdirectories with native 
[ZED Camera `.svo`](https://github.com/stereolabs/zed-sdk)) files.


