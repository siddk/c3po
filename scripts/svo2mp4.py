"""
svo2mp4.py

Bulk export script for converting a day's worth of demonstration SVO files to MP4 videos, with the ability to specify
which stereo stream to dump for each camera (e.g., Left-Only, Right-Only).
    => Note :: Requires ZED SDK (w/ CUDA) and `pyzed.sl`

Run with `python scripts/svo2mp4.py  --in <SVO-PATH> --out <MP4-PATH>

References:
    - https://github.com/AlexanderKhazatsky/R2D2/blob/main/scripts/post_processing/svo_to_mp4.py
    - https://github.com/stereolabs/zed-sdk/blob/master/recording/export/svo/python/svo_export.py
"""
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pyrallis

from c3po.export.svo import export_mp4


# fmt: off
@dataclass
class SVOConvertConfig:
    full_day_path: str              # Path to `lab-uploads/<LAB>/<YYYY-MM-DD>` directory to bulk export
    view: str = "left"              # View to dump in MP4 in < left | right > (stereo support pending)


# fmt: on
@pyrallis.wrap()
def svo2mp4(cfg: SVOConvertConfig) -> None:
    print(f"[*] Converting SVO Files at `{cfg.full_day_path}` to MP4 with view = `{cfg.view}`")

    # Start Iterating through Individual Demonstration Directories
    successful_exports, failed_exports = defaultdict(list), defaultdict(list)
    for demo_dir in Path(cfg.full_day_path).iterdir():
        print(f"\t=> Processing Demonstration at `{demo_dir}`")
        mp4_directory = demo_dir / "recordings" / "MP4"
        os.makedirs(mp4_directory, exist_ok=True)

        # Iterate through each SVO file and export!
        svo_files = list((demo_dir / "recordings" / "SVO").iterdir())
        assert len(svo_files) == 3, f"Each SVO directory should only have 3 SVO files - see `{demo_dir}`!"
        for svo in svo_files:
            mp4_out = export_mp4(svo, mp4_directory, view=cfg.view, show_progress=True)
            if mp4_out is not None:
                successful_exports[str(demo_dir)].append(str(mp4_out))
            else:
                failed_exports[str(demo_dir)].append(str(mp4_out))

    # TODO => Verification on Successful / Unsuccessful Exports!
    failed_demonstrations = "\n".join(list(failed_exports.keys()))
    print(f"Failed Demonstrations:\n{failed_demonstrations}")

    # # Create Output Path
    # mp4_directory = Path(cfg.svo_in).parent.parent / "MP4"
    # mp4_out = mp4_directory / f"{Path(cfg.svo_in).stem}.mp4"
    # os.makedirs(mp4_directory, exist_ok=True)
    #
    # # Configure PyZED --> set mostly from SVO Path, don't convert in realtime!
    # initial_parameters = sl.InitParameters()
    # initial_parameters.set_from_svo_file(cfg.svo_in)
    # initial_parameters.svo_real_time_mode = False
    # initial_parameters.coordinate_units = sl.UNIT.MILLIMETER
    #
    # # Create ZED Camera Object & Open SVO File
    # zed = sl.Camera()
    # err = zed.open(initial_parameters)
    # if err != sl.ERROR_CODE.SUCCESS:
    #     print(f"Error loading SVO: `{err}`")
    #     zed.close()
    #     exit(1)
    #
    # # Get Image Size
    # resolution = zed.get_camera_information().camera_configuration.resolution
    # width, height = resolution.width, resolution.height
    #
    # # Create ZED Image Containers
    # assert cfg.view in {"left", "right", "depth"}, f"Invalid View to Export `{cfg.view}`!"
    # img_container = sl.Mat()
    #
    # # Create a VideoWriter with the MP4V Codec
    # video_writer = cv2.VideoWriter(
    #     str(mp4_out),
    #     cv2.VideoWriter_fourcc(*"mp4v"),
    #     zed.get_camera_information().camera_configuration.fps,
    #     (width, height),
    # )
    #
    # # Error Handling
    # if not video_writer.isOpened():
    #     print(f"Error Opening CV2 Video Writer; check the MP4 path `{mp4_out}` and permissions!")
    #     zed.close()
    #     exit(1)
    #
    # # Start SVO Conversion
    # n_frames = zed.get_svo_number_of_frames()
    # rt_parameters, pbar = sl.RuntimeParameters(), tqdm(total=n_frames, desc="Converting SVO")
    # while True:
    #     if zed.grab(rt_parameters) == sl.ERROR_CODE.SUCCESS:
    #         svo_position = zed.get_svo_position()
    #         zed.retrieve_image(
    #             img_container, {"left": sl.VIEW.LEFT, "right": sl.VIEW.RIGHT, "depth": sl.VIEW.DEPTH}[cfg.view]
    #         )
    #
    #         # Copy image data into VideoWriter after converting to RGB
    #         rgb = cv2.cvtColor(img_container.get_data(), cv2.COLOR_RGBA2RGB)
    #         video_writer.write(rgb)
    #
    #         # Update Progress
    #         pbar.update()
    #
    #         # Check if we've reached the end of the video
    #         if svo_position >= (n_frames - 1):
    #             break
    #
    # # Cleanup
    # pbar.close()
    # video_writer.release()
    # zed.close()


if __name__ == "__main__":
    svo2mp4()
