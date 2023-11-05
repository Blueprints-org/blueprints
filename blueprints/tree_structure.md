
# Main dependencies
## Low level 0
* productdata
* codes (data, table, equations, figures)
* materials
* geometry

## Level 1
* Structural sections
  * materials
  * geometry
  * product data

* soils
  * materials

## level 2
* Structural objects
  * materials
  * geometry
  * product data

## level 3
* checks
* External bindings


# Codes
## Sub directories
- EuroCode
  - EuroCode 1992-1-1
    - EuroCode 1992-1-1 versie

- cur
  - cur 166
    - cur 166 versie

## Content
* Equations --> Class of functions....
* Tables --> Class, dictionaries...
* Figures --> Class, dictionaries...

# Productdata
## Sub directories
- Steel profiles
  - HEA profiles
- Sheet pile profiles
- Pile systems
- Hexagon Bolts


## Content

* Data (SQL, .json, dictionaries etc.)
* Classes (HEA - Profile)

**QUESTION** Where to store the data?

Depends on the size of the data. If the data is small, it can be stored in a dictionary. 
If the data is large, it should be stored in a database.

Possible within each sub package, below productdata or external storage.

# Object definities

## Sub directories
* Structural
  * Nodes
  * Beams
  * Plates
  * Load
  * Load Combination
* Geometry
  * Points
  * Lines
  * Surfaces
  * Solids
* Materials
  * Steel
  * Concrete
  * Timber
* Sections 
  * Reinforcement
    * Reinforcement bars
    * Stirrups
  * ReinforcedConcreteCrossSections
    * Rectangular
    * Circular
* Geotechnical
  * Soil
  * SoilProfile
  * SoilLayer

# Checks
Combine data, geometry and loads to perform checks according to the codes.

## Sub directories
* Steel profile (Hea etc.)
* Circular hollow section
* Rectangular concrete section
* Circular concrete section


# Bindings
## Sub directories
* External
  * CEMS
  * Scia
  * Etc.