[![build][badge_thumbnail]][badge_link]

# colorx

An implementation of various algorithms for transferring the colors from a reference image to a
content image while preserving the qualitative appearance of the content image (color transfer).

<div align="center">
  <a href="https://github.com/dstein64/media/blob/main/colorx/content.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colorx/content_thumbnail.jpg?raw=true" height="218"/>
  </a>
  <a href="https://github.com/dstein64/media/blob/main/colorx/reference.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colorx/reference_thumbnail.jpg?raw=true" height="218"/>
  </a>
  <br>
  <a href="https://github.com/dstein64/media/blob/main/colorx/output.jpg?raw=true">
    <img src="https://github.com/dstein64/media/blob/main/colorx/output_thumbnail.jpg?raw=true" width="710"/>
  </a>
</div>

Installation
------------

#### Requirements

- Python 3.6 or greater (earlier versions may work, but were not tested)

#### Install

```sh
$ pip3 install colorx
```

#### Update

```sh
$ pip3 install --upgrade colorx
```

Command-Line Usage
------------------

The program can be used from the command line.

The general command line usage is shown below.

```sh
$ colorx [--method METHOD] CONTENT REFERENCE OUTPUT
```

`CONTENT` is the path to the content image, `REFERENCE` is the path to the style image, and `OUTPUT`
is the path to save the output image.

`METHOD` specifies the color transfer algorithm. The following methods are supported:

1. `lhm` Linear Histogram Matching [1]
2. `pccm` Principal Components Color Matching [2,3]
3. `reinhard` Reinhard et al. [4]
4. `cwct` Channel-Wise Color Transfer

If the launcher script was not installed within a directory on your PATH, colorx can be launched by
passing its module name to Python.

```sh
$ python3 -m colorx [--method METHOD] CONTENT REFERENCE OUTPUT
```

Library Usage
-------------

TODO

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

[badge_link]: https://github.com/dstein64/colorx/actions/workflows/build.yml
[badge_thumbnail]: https://github.com/dstein64/colorx/actions/workflows/build.yml/badge.svg
