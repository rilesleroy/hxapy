# A python implementaion for the HxA file format
This is an implementaion of the HxA 3D asset format.
The HxA file format was invented by Eskil Steenberg
in an effort to have a 3D file format you could 
implemented in a day with out much hassle.

If you want an overiew of HxA I recomend checking Eskil's Original
Video here: 
https://youtu.be/watch?v=jlNSbSutPZE

Also checkout the original HxA repo and C implementation herehere:
https://github.com/quelsolaar/HxA

This library was modeled after gingerbill's odin implementation of hxa which can be found here:
https://github.com/odin-lang/Odin/tree/master/core/encoding/hxa

# Installation
This library is being hosted on PYPI so you can install it by simply using

```pip install hxa```

You can test if everything is working import the library and give the `hxa.triangle()` function ago

```python
import hxa
triangle = hxa.triangle()
hxa.write_to_file("path/to/file.hxa", triangle)
```

If the program spits out a file you are good to go.

# Usage
This library was made to help with the creation of HxA exporters and importers for popular DCC tools.
Eskil's original C implementation (and collection of converters) were great at demoing the format but
wasnt great for tool integration. I'm hoping that by providing a way to use the HxA format in native python
it would help to etablish a larger ecosystem of tools and addons around the format.

# 0.1.0 checklist
- [x] The basic "in-memory" class composition of the file.
- [x] writing to a file
- [ ] reading from a file - (Open a PR if you need this ASAP, otherwise I'll be working on a blender exporter first)