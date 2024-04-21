# Houdini scene collector

Collector parses a HIP file and USD files recursively and automatically:
- create a copy of them in another folder so you can easily send the whole scene with all dependencies 
- send via rsync (not implemented yet)
- upload to amazon-like S3 (not implemented yet)
- store them into an archive or library (not implemented yet)

### Collector Dialog accepts drag-n-drop of files and even folders you want to add mannualy.

## To install:
Just copy repo contents to your `~/Documents/houdini19.5` folder.

## Structure:
- You can find PyQT samples in `scripts/python/ui` module.

- You can find HIP and USD parsing logic inside of `scripts/python/hip_parser.py` and `scripts/python/usd_parser.py`.
