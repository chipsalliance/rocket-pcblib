#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Original nominal SAMZO C4B1802110 STEP; run with FreeCAD Python.

Dimensions and materials: C4B*** A1 drawing (2018-06-12), ordered H=1.8 mm.
https://atta.szlcsc.com/upload/public/pdf/source/20250721/FC1E3B81B3AA2D2C01374348D55797E2.pdf
Body 3.5 x 3.0; lead span 4.6; lead width 0.5; row pitch 1.5;
cap height 1.35; actuator diameter 1.7; metal thickness 0.15 mm.
Seating plane Z=0, pin 1 negative X / positive Y. Black LCP and
silver plated metal follow the material table. RGB shades, hidden body
construction and lead bends are display approximations, not toleranced
manufacturing geometry. No vendor logo or source-model geometry is used.
"""
from pathlib import Path
import sys
import FreeCAD as App
import Import
import Part


def build(output):
    doc = App.newDocument('SAMZO_C4B1802110')
    objects = []

    def add(name, shape, color):
        assert shape.isValid() and len(shape.Solids) == 1, name
        obj = doc.addObject('PartDesign::Feature', name)
        obj.Shape = shape.copy()
        objects.append((obj, [color] * len(shape.Faces)))
        return shape

    metal = (0.72, 0.72, 0.72)
    black = (0.10, 0.10, 0.10)
    leads = []
    for n, x, y in [(1, -1, .75), (2, 1, .75),
                    (3, -1, -.75), (4, 1, -.75)]:
        foot = Part.makeBox(.55, .5, .15, App.Vector(1.75, y-.25, 0))
        upright = Part.makeBox(.15, .5, .55, App.Vector(1.75, y-.25, .15))
        shoulder = Part.makeBox(.4, .5, .15, App.Vector(1.5, y-.25, .55))
        lead = foot.fuse(upright).fuse(shoulder).removeSplitter()
        if x < 0:
            lead.rotate(App.Vector(0, y, 0), App.Vector(0, 0, 1), 180)
        leads.append(add('Terminal_'+str(n), lead, metal))
    body = Part.makeBox(3.5, 3, 1.05, App.Vector(-1.75, -1.5, .15))
    body = body.cut(Part.makeCompound(leads)).removeSplitter()
    add('Black_LCP_body', body, black)
    cap = Part.makeBox(3.5, 3, .15, App.Vector(-1.75, -1.5, 1.2))
    hole = Part.makeCylinder(.87, .17, App.Vector(0, 0, 1.19))
    add('Metal_cover', cap.cut(hole).removeSplitter(), metal)
    add('Black_LCP_actuator', Part.makeCylinder(.85, .6,
                                               App.Vector(0, 0, 1.2)), black)
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
