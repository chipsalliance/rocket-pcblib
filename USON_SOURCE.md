# USON-10 land patterns and models

The two footprints use separate manufacturer recommendations.

- TI TPD4E02B04DQA: `CHIPSAlliance_Package_SON:USON-10_2.5x1.0mm_P0.5mm`.
- TECH PUBLIC RCLAMP0524P: `CHIPSAlliance_Package_SON:TechPublic_USON-10_2.5x1.0mm_P0.5mm`.
Both have a 2.5 x 1.0 mm body and 0.5 mm pitch.
Dimensions below use the existing horizontal footprint orientation.

| Parameter, mm | TI DQA0010A | TECH PUBLIC DFN2510-10 |
| --- | --- | --- |
| Signal copper | 0.20 x 0.565 | 0.20 x 0.675 |
| Signal row centers | Y = +/-0.4175 | Y = +/-0.4375 |
| Ground copper | Two 0.40 x 0.565 pads | One continuous 0.40 x 1.55 strip |
| Signal paste | Same as copper | Same as copper |
| Ground paste | Two 0.36 x 0.565 apertures | One 0.40 x 1.55 aperture |

TI copper and paste corners use R0.05.
The TECH PUBLIC rectangular land pattern takes priority under KLC F4.1.
Its ground strip consists of two touching rectangular pads numbered 3 and 8.
Both pads must connect to the same GND net. Neither pin number is omitted.
The manufacturer land pattern takes priority over the common-number rule in KLC F4.3.
The ground paste is a separate aperture. TECH PUBLIC does not specify its stencil dimensions.

Footprint mask expansion remains inherited from the board.
TI prefers NSMD and allows expansion up to 0.07 mm in its example.
This is an upper bound, not a fixed process setting.

The models are generated from manufacturer dimensions and licensed under Apache-2.0.
Both use 0.20 mm signal terminals and 0.40 mm ground terminals.
The TI model uses the 0.55 mm maximum height and midpoint terminal dimensions.
Its 0.02 mm body standoff is illustrative because the drawing does not specify it.
The TECH PUBLIC model uses the dimensional table's nominal height of 0.58 mm and standoff of 0.03 mm.
Pin marks and colors are illustrative. Both models use Z=0 at the contact plane.

For designs using TECH PUBLIC RCLAMP0524P, select the TECH PUBLIC footprint explicitly.
Confirm the purchased manufacturer before updating a board.
The two land patterns are not interchangeable solely because their package outlines match.

Sources:

- [TI TPD4E02B04, DQA0010A package and land/stencil drawings](https://www.ti.com/lit/ds/symlink/tpd4e02b04.pdf).
- [TECH PUBLIC RCLAMP0524P, page 5](https://atta.szlcsc.com/upload/public/pdf/source/20210810/AE3DE9AC94AD2A317FD9BEA10653400F.pdf).

[TI generator](https://github.com/vowstar/rocket-pcblib-generators/blob/4bfd24b7176961a652fc065531e61c8c10dc5689/models/CHIPSAlliance_Package_SON/USON-10_2.5x1.0mm_P0.5mm/generate.py).
[TECH PUBLIC generator](https://github.com/vowstar/rocket-pcblib-generators/blob/4bfd24b7176961a652fc065531e61c8c10dc5689/models/CHIPSAlliance_Package_SON/TechPublic_USON-10_2.5x1.0mm_P0.5mm/generate.py).
