# Average Edge Length

[![Version](https://img.shields.io/docker/v/fnndsc/pl-obj-avg-edge-length?sort=semver)](https://hub.docker.com/r/fnndsc/pl-obj-avg-edge-length)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-obj-avg-edge-length)](https://github.com/FNNDSC/pl-obj-avg-edge-length/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-obj-avg-edge-length/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-obj-avg-edge-length/actions/workflows/ci.yml)

`pl-obj-avg-edge-length` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

...

## Installation

`pl-obj-avg-edge-length` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-obj-avg-edge-length)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-obj-avg-edge-length` as a container:

```shell
singularity exec docker://fnndsc/pl-obj-avg-edge-length edgy [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-obj-avg-edge-length edgy --help
```

## Examples

`edgy` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-obj-avg-edge-length:latest edgy [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-obj-avg-edge-length .
```

### Running

Mount the source code `edgy.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/edgy.py:/usr/local/lib/python3.10/site-packages/edgy.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-obj-avg-edge-length edgy /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-obj-avg-edge-length:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-obj-avg-edge-length:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-obj-avg-edge-length:1.2.3 .
docker push docker.io/fnndsc/pl-obj-avg-edge-length:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-obj-avg-edge-length:dev chris_plugin_info > chris_plugin_info.json
```

