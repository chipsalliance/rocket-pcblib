#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Original nominal WS2812B-1313-V6 STEP; run with FreeCAD Python.

Worldsemi V1.3, page 2 (URL retains the older version string):
https://www.world-semi.com/downloads/datasheets/en/ws2812b-1313-v6-1.0.pdf
Body 1.3 x 1.3 x 0.65 mm; contact squares 0.4 mm and row gap 0.4 mm.
Symmetric 0.8 mm column pitch is inferred from the drawing, not explicitly
dimensioned. Pin 1 negative X / positive Y; board seating plane Z=0.
The datasheet draws transparent encapsulation over dies/leadframe. Internal
geometry, resin subdivision, metallization thickness and RGB shades below
are display approximations. They do not specify the production construction.
No logo, wire routing or unverified bottom polarity mark is added.
"""
from pathlib import Path
import sys
import FreeCAD as App
import Import
import Part


def build(output):
    doc = App.newDocument('WS2812B_1313_V6')
    objects = []

    def add(name, shape, color):
        assert shape.isValid() and len(shape.Solids) == 1, name
        obj = doc.addObject('PartDesign::Feature', name)
        obj.Shape = shape.copy()
        objects.append((obj, [color] * len(shape.Faces)))
        return shape

    metal = (0.72, 0.72, 0.72)
    solids = []
    for n, x, y in [(1, -.4, .4), (2, -.4, -.4),
                    (3, .4, -.4), (4, .4, .4)]:
        solids.append(add('Terminal_'+str(n), Part.makeBox(.4, .4, .06,
                          App.Vector(x-.2, y-.2, 0)), metal))
    substrate = Part.makeBox(1.3, 1.3, .18, App.Vector(-.65, -.65, 0))
    add('Base', substrate.cut(Part.makeCompound(solids)).removeSplitter(),
        (.84, .84, .80))
    ic = add('Controller_die', Part.makeBox(.30, .48, .08,
             App.Vector(.05, -.24, .18)), (.16, .16, .18))
    internal = [ic]
    for label, y, color in [('R', .28, (.40, .10, .10)),
                           ('G', 0, (.12, .30, .16)),
                           ('B', -.28, (.10, .17, .36))]:
        internal.append(add('Die_'+label, Part.makeBox(.19, .19, .08,
                        App.Vector(-.36, y-.095, .18)), color))
    resin = Part.makeBox(1.3, 1.3, .47, App.Vector(-.65, -.65, .18))
    resin = resin.cut(Part.makeCompound(internal)).removeSplitter()
    # FreeCAD's RGBA STEP export uses alpha=1 for opaque material.
    # The exported transparency is verified by importing the resulting STEP.
    add('Clear_encapsulation', resin, (.93, .95, .96, .22))
    doc.recompute()
    output.parent.mkdir(parents=True, exist_ok=True)
    Import.export(objects, str(output))
    raw = output.read_text().replace('HEADER;\n',
        'HEADER;\n/* SPDX-License-Identifier: Apache-2.0\n'
        f' * Source: {Path(__file__).name}; nominal dimensions and display\n'
        ' * approximations are documented in that original model source. */\n', 1)
    output.write_text('\n'.join(x.rstrip() for x in raw.splitlines())+'\n')
    App.closeDocument(doc.Name)
    print(output)


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_suffix('.step'))
