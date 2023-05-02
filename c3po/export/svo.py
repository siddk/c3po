"""
svo.py

Export utilities for converting SVO files to MP4 videos, with extra utilities for configuring which camera stream(s) in
each stereo feed to dump (e.g., Left, Right), where to write MP4s, and other useful helper functions.
    => Note :: Requires ZED SDK (w/ CUDA) and Python Bindings (`pyzed.sl`)

References:
    - https://github.com/AlexanderKhazatsky/R2D2/blob/main/scripts/post_processing/svo_to_mp4.py
    - https://github.com/stereolabs/zed-sdk/blob/master/recording/export/svo/python/svo_export.py
"""
from pathlib import Path
from typing import Optional

import cv2
import pyzed.sl as sl
from tqdm import tqdm


def export_mp4(svo_input: Path, mp4_directory: Path, view: str = "left", show_progress: bool = False) -> Optional[Path]:
    """Reads and SVO file, dumping the exported MP4 to the desired directory --> returning full MP4 path."""
    mp4_out = mp4_directory / f"{svo_input.stem}.mp4"

    # Configure PyZED --> set mostly from SVO Path, don't convert in realtime!
    initial_parameters = sl.InitParameters()
    initial_parameters.set_from_svo_file(str(svo_input))
    initial_parameters.svo_real_time_mode = False
    initial_parameters.coordinate_units = sl.UNIT.MILLIMETER

    # Create ZED Camera Object & Open SVO File
    zed = sl.Camera()
    err = zed.open(initial_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"Error loading SVO: `{err}`")
        zed.close()
        return None

    # Get Image Size
    resolution = zed.get_camera_information().camera_configuration.resolution
    width, height = resolution.width, resolution.height

    # Create ZED Image Containers
    assert view in {"left", "right"}, f"Invalid View to Export `{view}`!"
    img_container = sl.Mat()

    # Create a VideoWriter with the MP4V Codec
    video_writer = cv2.VideoWriter(
        str(mp4_out),
        cv2.VideoWriter_fourcc(*"mp4v"),
        zed.get_camera_information().camera_configuration.fps,
        (width, height),
    )
    if not video_writer.isOpened():
        print(f"Error Opening CV2 Video Writer; check the MP4 path `{mp4_out}` and permissions!")
        zed.close()
        return None

    # SVO Export
    n_frames, rt_parameters = zed.get_svo_number_of_frames(), sl.RuntimeParameters()
    if show_progress:
        pbar = tqdm(total=n_frames, desc="Exporting SVO Frames")

    # Read and Transcode all Frames
    while True:
        if zed.grab(rt_parameters) == sl.ERROR_CODE.SUCCESS:
            svo_position = zed.get_svo_position()
            zed.retrieve_image(img_container, {"left": sl.VIEW.LEFT, "right": sl.VIEW.RIGHT}[view])

            # Copy image data into VideoWrite after converting to RGB
            rgb = cv2.cvtColor(img_container.get_data(), cv2.COLOR_RGBA2RGB)
            video_writer.write(rgb)

            # Update Progress
            if show_progress:
                pbar.update()

            # Check if we've reached the end of the video
            if svo_position >= (n_frames - 1):
                break

    # Cleanup & Return
    video_writer.release()
    zed.close()
    if show_progress:
        pbar.close()

    return mp4_out
