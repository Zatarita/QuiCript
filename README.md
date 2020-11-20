# QuiCript
CEA/H2A de/compressor.

QuiCript is a collection of python scripts that aims to be an all-in-one solution your halo compression needs. Currently it has been tested on PC versions, it is currently unknown what other formats may exist on console, research will be done.

you can access each module independantly with their respective modules, or run the QuiCript as a CLI style script. The syntax is as follows:

```
"python QuiCript.py 'h1a'/'h2a'/'h2am' -c/-d 'path/to/file' 'path/to/second/file' ... 'path/to/last/file' "
  h1a  - Halo Anniversary
  h2a  - Halo 2 Anniversary
  h2am - Halo 2 Anniversary Map
```

each module independantly expects either data, or a path to be passed to the function. If a file path is passed, it will load the data from the path.

```python
from h1a import h1a_compress

compressed_data = h1a_compress("path/to/file")
```

```python
from h2am import h2am_decompress

data = open("halo2a.map", "rb").read()
decompressed_data = h2am_decompress("data")
```

This is a side project; however, i will dedicate some time here and there
