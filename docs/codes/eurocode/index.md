# Eurocode Standards

The Eurocode standards form the backbone of structural design across Europe, providing harmonized technical rules for the design of construction works. Blueprints implements key formulas, tables, and provisions from these comprehensive design codes.

## About Eurocodes

The Eurocodes are a set of 10 European Standards (EN) that provide common structural design rules for everyday use for the design of whole structures and component products of both a traditional and innovative nature. They cover the design of buildings and civil engineering works in reinforced concrete, steel, composite steel and concrete, timber, masonry, and aluminum.

## Implemented Standards

### Concrete Design (EN 1992)

**EN 1992: Design of concrete structures**

- **[EN 1992-1-1:2004](en_1992_1_1_2004/formulas.md)** - General rules and rules for buildings  
  Comprehensive design rules for reinforced and prestressed concrete structures including material properties, structural analysis, and design verification.

- **[EN 1992-2:2005](en_1992_2_2005/formulas.md)** - Concrete bridges - Design and detailing rules  
  Specialized provisions for concrete bridge design including additional requirements for durability and construction.

- **[NEN-EN 1992-1-1:2020](nen_en_1992_1_1_2020/formulas.md)** - General rules and rules for buildings (Dutch National Annex)  
  Dutch implementation with national choices for the application of EN 1992-1-1.

### Steel Design (EN 1993)

**EN 1993: Design of steel structures**

- **[EN 1993-1-1:2005](en_1993_1_1_2005/formulas.md)** - General rules and rules for buildings  
  Fundamental rules for the design of steel structures including material properties, structural analysis, and member design.

- **[EN 1993-1-8:2005](en_1993_1_8_2005/formulas.md)** - Design and calculation of connections  
  Detailed rules for the design of bolted, welded, and pinned connections in steel structures.

- **[EN 1993-1-9:2005](en_1993_1_9_2005/formulas.md)** - Fatigue design  
  Rules for the assessment of fatigue resistance of steel structures and components.

- **[EN 1993-5:2007](en_1993_5_2007/formulas.md)** - Piling design  
  Specific rules for the design of steel piles and pile foundations.

### Timber Design (EN 1995)

**EN 1995: Design of timber structures**

- **[EN 1995-1-1:2023](en_1995_1_1_2023/formulas.md)** - Design of timber structures, General rules and rules for buildings  
  General rules for the design of timber structures including material properties, structural analysis, and member design for buildings.

### Geotechnical Design (EN 1997)

**EN 1997: Geotechnical design**

- **[NEN 9997-1+C2:2017](nen_9997_1_c2_2017/formulas.md)** - Dutch geotechnical design rules  
  Dutch national standard based on EN 1997 for geotechnical design including soil investigations, foundation design, and ground improvement.

## Implementation Features

Each Eurocode implementation in Blueprints includes:

- **Formula tracking**: Complete catalog of implemented formulas with status indicators
- **Table implementations**: Design tables and coefficient lookups
- **Figure digitization**: Where applicable, charts and nomograms are implemented as functions
- **Cross-references**: Links between related formulas and dependencies
- **Validation**: Comprehensive test coverage against worked examples

## Implementation Status

The implementation status is tracked using:
- ✅ - Fully implemented and tested
- ❌ - Not yet implemented
- Object names reference the corresponding Python classes in Blueprints

Each standard's documentation provides detailed tracking of formula implementation progress, with object names referencing the corresponding Python classes in Blueprints.
