"""
ingest.py

Initial Data Ingestion Test (GDrive --> Normalize --> S3) for trial experiments [5/1/23].
"""

# Download IRIS, ILIAD, and Gupta Lab Data for Individual Days
#   - IRIS (4/13): https://drive.google.com/drive/folders/1JkW3X88Cx2TdBJlmSIVO7Vp5jR3udQPI
#   - ILIAD (4/19): https://drive.google.com/drive/folders/1faRYHgF9AK4ndlOhPR7bUzkfKJ1mDKKT
#   - Gupta Lab (4/20): https://drive.google.com/drive/folders/1qg_nNnGn_XNYsehsaDjnbhxlu9hnvfdL
#
# Run from `c3po/data/lab-uploads`:
#   gdown https://drive.google.com/drive/folders/1JkW3X88Cx2TdBJlmSIVO7Vp5jR3udQPI -O iris/2023-04-13 --folder
#   gdown https://drive.google.com/drive/folders/1faRYHgF9AK4ndlOhPR7bUzkfKJ1mDKKT -O iliad/2023-04-19 --folder
#   gdown https://drive.google.com/drive/folders/1qg_nNnGn_XNYsehsaDjnbhxlu9hnvfdL -O gupta-lab/2023-04-20 --folder
