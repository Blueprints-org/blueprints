**EN 1993-1-9 - May 2005
Eurocode 3: Design of steel structures
Part 1-9: Fatigue**

The table presents a list of figures from the Eurocode 3 standards for steel structures, tracking their implementation status (:x: or :heavy_check_mark:)
and any pertinent remarks. The 'Object Name' column references the corresponding Python entities inside of Blueprints.

Only the figures implemented so far are listed; the complete figure inventory of the standard is still to be added.

| Figure number | Done | Remarks | Object name |
|:--------------|:----:|:--------|:------------|
| 7.1           | :heavy_check_mark: | Fatigue strength curve for direct stress ranges. Selected through `FatigueStrengthCurve.FIG_7_1`. | Fig7NominalStressRange, Fig7NumberOfCycles, Fig7ConstantAmplitudeFatigueLimit, Fig7CutOffLimit |
| 7.2           | :heavy_check_mark: | Fatigue strength curve for shear stress ranges. Selected through `FatigueStrengthCurve.FIG_7_2`; the single slope runs straight to the cut-off limit, so there is no constant amplitude fatigue limit. | Fig7NominalStressRange, Fig7NumberOfCycles, Fig7CutOffLimit |
