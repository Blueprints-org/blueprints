**EN 1993-1-9:2025
Eurocode 3: Design of steel structures
Part 1-9: Fatigue**

The table presents a list of figures from the Eurocode 3 standards for steel structures, tracking their implementation status (:x: or :heavy_check_mark:)
and any pertinent remarks. The 'Object Name' column references the corresponding Python entities inside of Blueprints.

Only the figures implemented so far are listed; the complete figure inventory of the standard is still to be added.

| Figure number | Done | Remarks | Object name |
|:--------------|:----:|:--------|:------------|
| 8.1a          | :heavy_check_mark: | Non-welded details, light notch effect. Selected through `FatigueStrengthCurve.FIG_8_1A`. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit, Fig8CutOffLimit |
| 8.1b          | :heavy_check_mark: | Non-welded details, sharp notch effect. Selected through `FatigueStrengthCurve.FIG_8_1B`. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit, Fig8CutOffLimit |
| 8.2a          | :heavy_check_mark: | Welded details, detail category 71 and above. Selected through `FatigueStrengthCurve.FIG_8_2A`. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit, Fig8CutOffLimit |
| 8.2b          | :heavy_check_mark: | Welded details, detail category below 71. Selected through `FatigueStrengthCurve.FIG_8_2B`. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit, Fig8CutOffLimit |
| 8.3           | :heavy_check_mark: | Lattice girder joints of hollow sections. Selected through `FatigueStrengthCurve.FIG_8_3`. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit, Fig8CutOffLimit |
| 8.4           | :heavy_check_mark: | Constructional details subject to shear stress. Selected through `FatigueStrengthCurve.FIG_8_4`; the single slope ends at the constant amplitude fatigue limit, so there is no separate cut-off limit. | Fig8NominalStressRange, Fig8NumberOfCycles, Fig8ConstantAmplitudeFatigueLimit |
