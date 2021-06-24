from contourpy import FillType, LineType
from .mpl_util import mpl_codes_to_offsets
import numpy as np


def filled_to_bokeh(filled, fill_type):
    xs = []
    ys = []
    if fill_type in (
        FillType.OuterOffsets, FillType.ChunkCombinedOffsets,
        FillType.OuterCodes, FillType.ChunkCombinedCodes):
        have_codes = \
            fill_type in (FillType.OuterCodes, FillType.ChunkCombinedCodes)

        for points, offsets in zip(*filled):
            if points is None:
                continue
            if have_codes:
                offsets = mpl_codes_to_offsets(offsets)
            xs.append([])  # New outer with zero or more holes.
            ys.append([])
            for i in range(len(offsets)-1):
                xys = points[offsets[i]:offsets[i+1]]
                xs[-1].append(xys[:, 0])
                ys[-1].append(xys[:, 1])
    elif fill_type in (
        FillType.ChunkCombinedCodesOffsets, FillType.ChunkCombinedOffsets2):
        for points, codes_or_offsets, outer_offsets in zip(*filled):
            if points is None:
                continue
            for j in range(len(outer_offsets)-1):
                if fill_type == FillType.ChunkCombinedCodesOffsets:
                    codes = codes_or_offsets[outer_offsets[j]:outer_offsets[j+1]]
                    offsets = mpl_codes_to_offsets(codes) + outer_offsets[j]
                else:
                    offsets = codes_or_offsets[outer_offsets[j]:outer_offsets[j+1]+1]
                xs.append([])  # New outer with zero or more holes.
                ys.append([])
                for k in range(len(offsets)-1):
                    xys = points[offsets[k]:offsets[k+1]]
                    xs[-1].append(xys[:, 0])
                    ys[-1].append(xys[:, 1])
    else:
        raise RuntimeError(f'Conversion of FillType {fill_type} to Bokeh is not implemented')

    return xs, ys


def lines_to_bokeh(lines, line_type):
    xs = []
    ys = []

    if line_type == LineType.Separate:
        for line in lines:
            xs.append(line[:, 0])
            ys.append(line[:, 1])
    elif line_type == LineType.SeparateCodes:
        for line in lines[0]:
            xs.append(line[:, 0])
            ys.append(line[:, 1])
    elif line_type in (LineType.ChunkCombinedCodes, LineType.ChunkCombinedOffsets):
        for points, offsets in zip(*lines):
            if points is None:
                continue
            if line_type == LineType.ChunkCombinedCodes:
                offsets = mpl_codes_to_offsets(offsets)

            for i in range(len(offsets)-1):
                line = points[offsets[i]:offsets[i+1]]
                xs.append(line[:, 0])
                ys.append(line[:, 1])
    else:
        raise RuntimeError(f'Conversion of LineType {line_type} to Bokeh is not implemented')

    return xs, ys