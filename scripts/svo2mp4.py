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


if __name__ == "__main__":
    svo2mp4()
