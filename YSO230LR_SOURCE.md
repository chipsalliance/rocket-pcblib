# YSO230LR model dimensions and license

Dimensions come from the [YXC YSO230LR datasheet, page 2](https://www.yxc.hk/uploadfiles/2025/10/YXC-YSO230LR.pdf),
retrieved for the 2026-10-20 library review:

| Parameter | Model |
| --- | --- |
| Body | 3.2 × 2.5 mm, oriented 2.5 × 3.2 mm on this footprint |
| Overall height | 1.2 mm, the datasheet maximum |
| Bottom contacts | 0.6 × 0.8 mm |
| Longitudinal terminal pitch | 1.2 mm |
| Contact plane | Z = 0 |
| Pin 1 | Upper left in KiCad top view |
| Footprint model transform | Offset/rotation zero, scale one |

This is an assembly-envelope model. Ceramic, lid, and terminal thicknesses
(1.05, 0.10, and 0.05 mm) and display colors are illustrative; those individual
values are not specified by YXC. Body outline dimensions and contact geometry
follow the drawing. The model omits logos, engraving, and unspecified small
edge details. It does not change the existing PCB land pattern.

The original model is distributed under this repository's
Apache-2.0 license. The manufacturer's datasheet remains the manufacturer's
documentation; it is linked, not included here.

[FreeCAD generator](https://github.com/vowstar/rocket-pcblib-generators/blob/4bfd24b7176961a652fc065531e61c8c10dc5689/models/CHIPSAlliance_Oscillator/Oscillator_SMD_YXC_YSO230LR-6Pin_3.2x2.5mm/generate.py).
