#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the companion STEP with FreeCAD's Python modules (no GUI needed).

Run with a Python interpreter able to import FreeCAD, Part and Import.
Optional first argument: output STEP path; default: next to this source file.

Geometry: GigaDevice GD25LQ128E datasheet, section 10.5, page 65:
https://atta.szlcsc.com/upload/public/pdf/source/20211122/9F6E477CE95D33C1850BF40E75C00EA5.pdf
All dimensions are nominal millimetres, not maximum assembly envelopes.
Pin 1 is at negative X / positive Y in MCAD coordinates (KiCad top left).
The seating plane is Z=0. No footprint scaling or alignment is necessary.

The datasheet does not dimension the EP corner chamfer, pin-1 recess or
mould edge bevel, nor specify RGB values. These are display approximations.
The plastic is charcoal; plated contacts are neutral silver-grey. No logos.
This is an original model, not a modification of a vendor or KiCad STEP.
"""
from pathlib import Path
import sys

import FreeCAD as App
import Import
import Part

BODY_X, BODY_Y = 6.0, 5.0
HEIGHT, STANDOFF, METAL_HEIGHT = 0.75, 0.02, 0.203
PITCH, LEAD_WIDTH, LEAD_LENGTH = 1.27, 0.40, 0.60
EP_X, EP_Y = 3.40, 4.00
PLASTIC = (0.12, 0.12, 0.12)
METAL = (0.75, 0.75, 0.75)
EDGE_BEVEL, EP_CHAMFER = 0.04, 0.30
MARK_RADIUS, MARK_DEPTH = 0.16, 0.035


def lead_shape(x_side, y):
    """Flat outer end and semicircular inner end, as in the package drawing."""
    radius = LEAD_WIDTH / 2
    outer_x = -BODY_X / 2
    round_x = outer_x + LEAD_LENGTH - radius
    square = Part.makeBox(LEAD_LENGTH - radius, LEAD_WIDTH, METAL_HEIGHT,
                          App.Vector(outer_x, y - radius, 0))
    circle = Part.makeCylinder(radius, METAL_HEIGHT, App.Vector(round_x, y, 0))
    shape = square.fuse(circle).removeSplitter()
    if x_side > 0:
        shape.rotate(App.Vector(0, y, 0), App.Vector(0, 0, 1), 180)
    return shape


def build(output):
    doc = App.newDocument('WSON8')
    objects = []

    def add(name, shape, color):
        assert shape.isValid() and len(shape.Solids) == 1, name
        obj = doc.addObject('PartDesign::Feature', name)
        obj.Label = name
        # Independent topology prevents shared CSG faces from stealing colours.
        obj.Shape = shape.copy()
        objects.append((obj, [color] * len(shape.Faces)))
        return shape

    pins = []
    for number in range(1, 9):
        side = -1 if number <= 4 else 1
        row = number - 1 if side < 0 else 8 - number
        y = (1.5 - row) * PITCH
        pins.append(add(f'Pin_{number}', lead_shape(side, y), METAL))

    x, y = EP_X / 2, EP_Y / 2
    points = [(-x, -y), (x, -y), (x, y), (-x + EP_CHAMFER, y),
              (-x, y - EP_CHAMFER), (-x, -y)]
    ep = Part.Face(Part.makePolygon([App.Vector(a, b, 0) for a, b in points]))
    ep = add('Exposed_pad', ep.extrude(App.Vector(0, 0, METAL_HEIGHT)), METAL)

    body = Part.makeBox(BODY_X, BODY_Y, HEIGHT - STANDOFF,
                        App.Vector(-BODY_X / 2, -BODY_Y / 2, STANDOFF))
    top_edges = [e for e in body.Edges if abs(e.BoundBox.ZMin - HEIGHT) < 1e-7]
    body = body.makeChamfer(EDGE_BEVEL, top_edges)
    # Subtract the embedded lead frame so the exported solids never overlap.
    body = body.cut(Part.makeCompound(pins + [ep])).removeSplitter()
    mark = Part.makeCylinder(MARK_RADIUS, MARK_DEPTH + 0.01,
                             App.Vector(-2.35, 1.85, HEIGHT - MARK_DEPTH))
    add('Moulded_body', body.cut(mark).removeSplitter(), PLASTIC)
    doc.recompute()
    output.parent.mkdir(parents=True, exist_ok=True)
    Import.export(objects, str(output))
    # Keep an explicit source/licence pointer inside the standalone STEP.
    step = output.read_text()
    note = ('/* SPDX-License-Identifier: Apache-2.0\n'
            f' * Source: {Path(__file__).name}\n'
            ' * GD25LQ128E WSON8 6x5mm nominal geometry; display details\n'
            ' * and colours are documented in the companion source.\n'
            ' */\n')
    step = step.replace('HEADER;\n', 'HEADER;\n' + note, 1)
    output.write_text('\n'.join(line.rstrip() for line in step.splitlines()) + '\n')
    App.closeDocument(doc.Name)
    print(output)


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix('.step'))
