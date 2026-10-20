# SPDX-License-Identifier: Apache-2.0
"""Build the YXC YSO230LR 3225 package in FreeCAD's Python console.

Source: https://www.yxc.hk/uploadfiles/2025/10/YXC-YSO230LR.pdf, page 2.
Body: 3.2 +/-0.1 x 2.5 +/-0.1 mm, 1.2 mm maximum total height.
Terminals: 0.6 x 0.8 mm, 1.2 mm longitudinal pitch.
The package is rotated to match this library's existing footprint:
pin 1 is upper left in the KiCad top view. Contact surface is Z=0.

This is a dimensional assembly-envelope model. The datasheet does not specify
individual ceramic/lid/metallization thicknesses. Their 0.05/1.05/0.10 mm split
and display colors are visual approximations; overall height uses the maximum.
No manufacturer logo or unsourced engraving is reproduced.
Run in FreeCAD GUI Python (offscreen is sufficient for STEP export).
"""
from pathlib import Path
import FreeCAD as App
import Part
import ImportGui


NAME = "Oscillator_SMD_YXC_YSO230LR-6Pin_3.2x2.5mm"


def build(output=None):
    directory = Path(output) if output else Path(__file__).resolve().parent.parent
    directory.mkdir(parents=True, exist_ok=True)
    doc = App.newDocument("YSO230LR3225")
    objects = []

    def box(label, size, corner, color):
        obj = doc.addObject("PartDesign::Feature", label)
        obj.Label = label
        obj.Shape = Part.makeBox(*size, App.Vector(*corner))
        obj.ViewObject.ShapeColor = color
        objects.append(obj)
        return obj

    box("Ceramic", (2.5, 3.2, 1.05), (-1.25, -1.6, 0.05), (0.24, 0.22, 0.19))
    box("MetalLid", (2.4, 3.1, 0.10), (-1.2, -1.55, 1.10), (0.72, 0.74, 0.75))
    for pin, x, y in [(1,-.85,1.2),(2,-.85,0),(3,-.85,-1.2),
                      (4,.85,-1.2),(5,.85,0),(6,.85,1.2)]:
        box(f"Terminal{pin}", (.8, .6, .05), (x-.4, y-.3, 0), (.78, .62, .25))
    doc.recompute()
    assert all(obj.Shape.isValid() and len(obj.Shape.Solids)==1 for obj in objects)
    compound = Part.makeCompound([obj.Shape for obj in objects])
    bounds = compound.BoundBox
    assert abs(bounds.XLength-2.5)<1e-7
    assert abs(bounds.YLength-3.2)<1e-7
    assert abs(bounds.ZLength-1.2)<1e-7 and abs(bounds.ZMin)<1e-7
    doc.saveAs(str(directory/(NAME+".FCStd")))
    ImportGui.export(objects, str(directory/(NAME+".step")))
    step = directory/(NAME+".step")
    step.write_text("\n".join(line.rstrip() for line in step.read_text().splitlines())+"\n")
    App.closeDocument(doc.Name)
    return directory/(NAME+".step")


if __name__ == "__main__":
    build()
