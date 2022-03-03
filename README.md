[![build][badge_thumbnail]][badge_link]

# colortrans

An implementation of various algorithms for transferring the colors from a reference image to a
content image while preserving the qualitative appearance of the content image (i.e., color
transfer).

<div align="center">
  <a href="https://github.com/dstein64/media/blob/main/colortrans/content.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colortrans/content_thumbnail.jpg?raw=true" height="218"/>
  </a>
  <a href="https://github.com/dstein64/media/blob/main/colortrans/reference.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colortrans/reference_thumbnail.jpg?raw=true" height="218"/>
  </a>
  <br>
  <a href="https://github.com/dstein64/media/blob/main/colortrans/output.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colortrans/output_thumbnail.jpg?raw=true" width="710"/>
  </a>
</div>

Installation
------------

#### Requirements

- Python 3.6 or greater (earlier versions may work, but were not tested)

#### Install

```sh
$ pip3 install colortrans
```

#### Update

```sh
$ pip3 install --upgrade colortrans
```

Command-Line Usage
------------------

The program can be used from the command line.

The general command line usage is shown below.

```sh
$ colortrans [--method METHOD] CONTENT REFERENCE OUTPUT
```

`CONTENT` is the path to the content image, `REFERENCE` is the path to the style image, and `OUTPUT`
is the path to save the output image.

`METHOD` specifies the color transfer algorithm. The following methods are supported:

1. `cwct` Channel-Wise Color Transfer
2. `lhm` Linear Histogram Matching [1] (default)
3. `pccm` Principal Components Color Matching [2,3]
4. `reinhard` Reinhard et al. [4]

If the launcher script was not installed within a directory on your PATH, colortrans can be launched by
passing its module name to Python.

```sh
$ python3 -m colortrans [--method METHOD] CONTENT REFERENCE OUTPUT
```

Library Usage
-------------

The algorithms can also be used directly from Python programs. Each of the methods listed above has
a corresponding function, `transfer_METHOD`, taking two NumPy arrays corresponding to the content
and reference image, respectively. The arrays have `HxWxC` data ordering (channels-last).

#### Example

```python
import colortrans
import numpy as np
from PIL import Image

# Load data
content = np.array(Image.open('/path/to/content.jpg').convert('RGB'))
reference = np.array(Image.open('/path/to/reference.jpg').convert('RGB'))

# Transfer colors using different algorithms
output_cwct = colortrans.transfer_cwct(content, reference)
output_lhm = colortrans.transfer_lhm(content, reference)
output_pccm = colortrans.transfer_pccm(content, reference)
output_reinhard = colortrans.transfer_reinhard(content, reference)

# Save outputs
Image.fromarray(output_cwct).save('/path/to/output_cwct.jpg')
Image.fromarray(output_lhm).save('/path/to/output_lhm.jpg')
Image.fromarray(output_pccm).save('/path/to/output_pccm.jpg')
Image.fromarray(output_reinhard).save('/path/to/output_reinhard.jpg')
```

References
----------

[1] Hertzmann, Aaron. "Algorithms for Rendering in Artistic Styles." Ph.D., New York University,
2001.

[2] Kotera, Hiroaki, Hung-Shing Chen, and Tetsuro Morimoto. "Object-to-Object Color Mapping by Image
Segmentation." In Color Imaging: Device-Independent Color, Color Hardcopy, and Graphic Arts IV,
3648:148–57. SPIE, 1998.

[3] Kotera, Hiroaki. "A Scene-Referred Color Transfer for Pleasant Imaging on Display." In IEEE
International Conference on Image Processing 2005, 2:II–5, 2005.

[4] Reinhard, Erik, Michael Adhikhmin, Bruce Gooch, and Peter Shirley. "Color Transfer between
Images." IEEE Computer Graphics and Applications 21, no. 5 (July 2001): 34–41.

[badge_link]: https://github.com/dstein64/colortrans/actions/workflows/build.yml
[badge_thumbnail]: https://github.com/dstein64/colortrans/actions/workflows/build.yml/badge.svg
