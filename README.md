# Houdini scene collector
![image](https://github.com/Al-Garifov/houdini-collector/assets/113169696/4ee590ed-4840-47d9-b648-92e6e486057f)


Collector parses a HIP file and USD files recursively and automatically:
- create a copy of them in another folder so you can easily send the whole scene with all dependencies 
- send via rsync (not implemented yet)
- upload to amazon-like S3 (not implemented yet)
- store them into an archive or library (not implemented yet)

### Collector Dialog accepts drag-n-drop of files and even folders you want to add mannualy.

## To install:
Just copy repo contents to your `~/Documents/houdini19.5` folder and turn on "Collector" shelf.

## Structure:
- You can find PyQT samples in `scripts/python/ui` module.

- You can find HIP and USD parsing logic inside of `scripts/python/hip_parser.py` and `scripts/python/usd_parser.py`.

___
## Special thanks to:
https://github.com/alexwheezy
