#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

import numpy as np

from bicpl import PolygonObj
from chris_plugin import chris_plugin, PathMapper

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


parser = ArgumentParser(description='Average edge length about each vertex of a surface mesh.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')
parser.add_argument('-f', '--filter', type=str, default='**/*.obj',
                    help='input file filter')
parser.add_argument('-s', '--suffix', type=str, default='.edgelen.txt',
                    help='output file suffix')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='Average Edge Length',
    category='Quality Control',  # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.filter, suffix=options.suffix)
    for input_file, output_file in mapper:
        process(input_file, output_file)


def process(input_file: Path, output_file: Path):
    data = average_lengths(input_file)
    mean = np.mean(data)
    std = np.std(data)
    np.savetxt(output_file, data)
    print(f'{input_file} -> {output_file}', end=' ')
    print(f'(min={np.min(data):.4f} max={np.max(data):.4f} mean={mean:.4f} std={std:.4f})')


def average_lengths(filename: Path) -> list[float]:
    obj = PolygonObj.from_file(filename)
    return [
        average_length_around(obj, index, neighbors)
        for index, neighbors in enumerate(obj.neighbor_graph())
    ]


def average_length_around(obj: PolygonObj, index: int, neighbors: tuple[set[int]]) -> float:
    coord = obj.point_array[index]
    l = [np.linalg.norm(coord - obj.point_array[n]) for n in neighbors]
    return np.mean(l)  # noqa: type


if __name__ == '__main__':
    main()
