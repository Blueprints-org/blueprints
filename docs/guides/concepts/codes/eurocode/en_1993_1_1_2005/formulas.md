**EN 1993-1-1 - May 2005
Eurocode 3: Design of steel structures  
Part 1-1: General rules and rules for buildings**

The table presents a list of formulas from the Eurocode 3 standards for steel structures, tracking their implementation
status (:x: or :heavy_check_mark:)
and any pertinent remarks. The 'Object Name' column references the corresponding Python entities inside of Blueprints.

The column with header 'NL' for example indicates whether a country specific implementation of the formula is 
implemented. Naming convention for country specific formulas is 'Form{formula_number}{CountryCode}'. E.g. for 
`Form5Dot1CriteriumDisregardSecondOrderEffects` the version specific to the Netherlands would be named
`Form5Dot1NLCriteriumDisregardSecondOrderEffects`.

Total of 108 formulas present.

| Formula number |        Done        | Remarks | Object name                                                                       |         NL         |
|:---------------|:------------------:|:--------|:----------------------------------------------------------------------------------|:------------------:|
| 2.1            |        :x:         |         |                                                                                   |        :x:         |
| 2.2            | :heavy_check_mark: |         | Form2Dot2CharacteristicValueResistance                                            |        :x:         |
| 5.1            | :heavy_check_mark: |         | Form5Dot1CriteriumDisregardSecondOrderEffects                                     | :heavy_check_mark: |
| 5.2            |        :x:         |         |                                                                                   |        :x:         |
| 5.3            |        :x:         |         |                                                                                   |        :x:         |
| 5.4            |        :x:         |         |                                                                                   |        :x:         |
| 5.5            |        :x:         |         |                                                                                   |        :x:         |
| 5.6            |        :x:         |         |                                                                                   |        :x:         |
| 5.7            | :heavy_check_mark: |         | Form5Dot7DisregardFrameSwayImperfections                                          |        :x:         |
| 5.8            | :heavy_check_mark: |         | Form5Dot8CheckSlenderness                                                         |        :x:         |
| 5.9            |        :x:         |         |                                                                                   |        :x:         |
| 5.10           |        :x:         |         |                                                                                   |        :x:         |
| 5.11           |        :x:         |         |                                                                                   |        :x:         |
| 5.12           |        :x:         |         |                                                                                   |        :x:         |
| 5.13           |        :x:         |         |                                                                                   |        :x:         |
| 5.14           |        :x:         |         |                                                                                   |        :x:         |
| 6.1            | :heavy_check_mark: |         | Form6Dot1ElasticVerification                                                      |        :x:         |
| 6.2            | :heavy_check_mark: |         | Form6Dot2UtilizationRatio                                                         |        :x:         |
| 6.3            | :heavy_check_mark: |         | Form6Dot3MinDeductionAreaStaggeredFastenerHoles                                   |        :x:         |
| 6.4            | :heavy_check_mark: |         | Form6Dot4AdditionalMoment                                                         |        :x:         |
| 6.5            | :heavy_check_mark: |         | Form6Dot5UnityCheckTensileStrength                                                |        :x:         |
| 6.6            | :heavy_check_mark: |         | Form6Dot6DesignPlasticResistanceGrossCrossSection                                |        :x:         |
| 6.7            | :heavy_check_mark: |         | Form6Dot7DesignUltimateResistanceNetCrossSection                                  |        :x:         |
| 6.8            | :heavy_check_mark: |         | Form6Dot8NetDesignTensionResistance                                               |        :x:         |
| 6.9            | :heavy_check_mark: |         | Form6Dot9CheckCompressionForce                                                    |        :x:         |
| 6.10           | :heavy_check_mark: |         | Form6Dot10NcRdClass1And2And3                                                      |        :x:         |
| 6.11           | :heavy_check_mark: |         | Form6Dot11NcRdClass4                                                              |        :x:         |
| 6.12           | :heavy_check_mark: |         | Form6Dot12CheckBendingMoment                                                      |        :x:         |
| 6.13           | :heavy_check_mark: |         | Form6Dot13MCRdClass1And2                                                          |        :x:         |
| 6.14           | :heavy_check_mark: |         | Form6Dot14MCRdClass3                                                              |        :x:         |
| 6.15           | :heavy_check_mark: |         | Form6Dot15McRdClass4                                                              |        :x:         |
| 6.16           | :heavy_check_mark: |         | Form6Dot16CheckFlangeWithFastenerHoles                                            |        :x:         |
| 6.17           | :heavy_check_mark: |         | Form6Dot17CheckShearForce                                                         |        :x:         |
| 6.18           | :heavy_check_mark: |         | Form6Dot18DesignPlasticShearResistance                                            |        :x:         |
| 6.18 A_v       | :heavy_check_mark: |         | Various equations                                                                 |        :x:         |
| 6.19           | :heavy_check_mark: |         | Form6Dot19CheckDesignElasticShearResistance                                       |        :x:         |
| 6.20           | :heavy_check_mark: |         | Form6Dot20ShearStress                                                             |        :x:         |
| 6.21           | :heavy_check_mark: |         | Form6Dot21ShearStressIOrHSection                                                  |        :x:         |
| 6.22           | :heavy_check_mark: |         | Form6Dot22CheckShearBucklingResistance                                            |        :x:         |
| 6.23           | :heavy_check_mark: |         | Form6Dot23CheckTorsionalMoment                                                    |        :x:         |
| 6.24           | :heavy_check_mark: |         | Form6Dot24TotalTorsionalMoment                                                    |        :x:         |
| 6.25           | :heavy_check_mark: |         | Form6Dot25CheckCombinedShearForceAndTorsionalMoment                               |        :x:         |
| 6.26           | :heavy_check_mark: |         | Form6Dot26VplTRdIOrHSection                                                       |        :x:         |
| 6.27           | :heavy_check_mark: |         | Form6Dot27VplTRdChannelSection                                                    |        :x:         |
| 6.28           | :heavy_check_mark: |         | Form6Dot28VplTRdHollowSection                                                     |        :x:         |
| 6.29           | :heavy_check_mark: |         | Form6Dot29ReducedYieldStrength                                                    |        :x:         |
| 6.29 (rho)     | :heavy_check_mark: |         | Form6Dot29Rho and Form6Dot29RhoWithTorsion                                        |        :x:         |
| 6.30           | :heavy_check_mark: |         | Form6Dot30ReducedPlasticResistanceMoment                                          |        :x:         |
| 6.31           | :heavy_check_mark: |         | Form6Dot31CheckBendingAndAxialForce                                               |        :x:         |
| 6.32           | :heavy_check_mark: |         | Form6Dot32MNrdRectangular                                                         |        :x:         |
| 6.33           | :heavy_check_mark: |         | Form6Dot33CheckAxialForceY                                                        |        :x:         |
| 6.34           | :heavy_check_mark: |         | Form6Dot34CheckAxialForceY                                                        |        :x:         |
| 6.35           | :heavy_check_mark: |         | Form6Dot35CheckAxialForceZ                                                        |        :x:         |
| 6.36           | :heavy_check_mark: |         | Form6Dot36MomentReduction                                                         |        :x:         |
| 6.37           | :heavy_check_mark: |         | Form6Dot37And38MomentReduction                                                    |        :x:         |
| 6.38           | :heavy_check_mark: |         | Form6Dot37And38MomentReduction                                                    |        :x:         |
| 6.38n          | :heavy_check_mark: |         | Form6Dot38N                                                                       |        :x:         |
| 6.38a          | :heavy_check_mark: |         | Form6Dot38A                                                                       |        :x:         |
| 6.39           | :heavy_check_mark: |         | Form6Dot39ReducedBendingMomentResistance                                          |        :x:         |
| 6.39 a_w       | :heavy_check_mark: |         | Form6Dot39awHollowSections and Form6Dot39awWeldedBoxSections                      |        :x:         |
| 6.40           | :heavy_check_mark: |         | Form6Dot40ReducedBendingMomentResistance                                          |        :x:         |
| 6.40 a_f       | :heavy_check_mark: |         | Form6Dot40afHollowSections and Form6Dot40afWeldedBoxSections                      |        :x:         |
| 6.41           | :heavy_check_mark: |         | Form6Dot41BiaxialBendingCheck                                                     |        :x:         |
| 6.42           | :heavy_check_mark: |         | Form6Dot42LongitudinalStressClass3CrossSections                                   |        :x:         |
| 6.43           | :heavy_check_mark: |         | Form6Dot43LongitudinalStressClass4CrossSections                                   |        :x:         |
| 6.44           | :heavy_check_mark: |         | Form6Dot44CombinedCompressionBendingClass4CrossSections                           |        :x:         |
| 6.45           | :heavy_check_mark: |         | Form6Dot45ReducedYieldStrength                                                    |        :x:         |
| 6.46           |        :x:         |         |                                                                                   |        :x:         |
| 6.47           |        :x:         |         |                                                                                   |        :x:         |
| 6.48           |        :x:         |         |                                                                                   |        :x:         |
| 6.49           |        :x:         |         |                                                                                   |        :x:         |
| 6.50           |        :x:         |         |                                                                                   |        :x:         |
| 6.51           |        :x:         |         |                                                                                   |        :x:         |
| 6.52           |        :x:         |         |                                                                                   |        :x:         |
| 6.53           |        :x:         |         |                                                                                   |        :x:         |
| 6.54           |        :x:         |         |                                                                                   |        :x:         |
| 6.55           |        :x:         |         |                                                                                   |        :x:         |
| 6.56           |        :x:         |         |                                                                                   |        :x:         |
| 6.57           |        :x:         |         |                                                                                   |        :x:         |
| 6.58           |        :x:         |         |                                                                                   |        :x:         |
| 6.59           |        :x:         |         |                                                                                   |        :x:         |
| 6.60           |        :x:         |         |                                                                                   |        :x:         |
| 6.61           |        :x:         |         |                                                                                   |        :x:         |
| 6.62           |        :x:         |         |                                                                                   |        :x:         |
| 6.63           |        :x:         |         |                                                                                   |        :x:         |
| 6.64           |        :x:         |         |                                                                                   |        :x:         |
| 6.65           |        :x:         |         |                                                                                   |        :x:         |
| 6.66           |        :x:         |         |                                                                                   |        :x:         |
| 6.67           |        :x:         |         |                                                                                   |        :x:         |
| 6.68           |        :x:         |         |                                                                                   |        :x:         |
| 6.69           |        :x:         |         |                                                                                   |        :x:         |
| 6.70           |        :x:         |         |                                                                                   |        :x:         |
| 6.71           | :heavy_check_mark: |         | FormADot2CriteriaBasedOnStressRangeLHS and FormADot2CriteriaBasedOnStressRangeRHS |        :x:         |
| 6.72           |        :x:         |         |                                                                                   |        :x:         |
| 6.73           |        :x:         |         |                                                                                   |        :x:         |
| 6.74           |        :x:         |         |                                                                                   |        :x:         |
| 6.75           |        :x:         |         |                                                                                   |        :x:         |
| BB.1           |        :x:         |         |                                                                                   |        :x:         |
| BB.2           |        :x:         |         |                                                                                   |        :x:         |
| BB.3           |        :x:         |         |                                                                                   |        :x:         |
| BB.4           |        :x:         |         |                                                                                   |        :x:         |
| BB.5           |        :x:         |         |                                                                                   |        :x:         |
| BB.6           |        :x:         |         |                                                                                   |        :x:         |
| BB.7           |        :x:         |         |                                                                                   |        :x:         |
| BB.8           |        :x:         |         |                                                                                   |        :x:         |
| BB.9           |        :x:         |         |                                                                                   |        :x:         |
| BB.10          |        :x:         |         |                                                                                   |        :x:         |
| BB.11          |        :x:         |         |                                                                                   |        :x:         |
| BB.12          |        :x:         |         |                                                                                   |        :x:         |
| BB.13          |        :x:         |         |                                                                                   |        :x:         |
| BB.14          |        :x:         |         |                                                                                   |        :x:         |
| BB.15          |        :x:         |         |                                                                                   |        :x:         |
| BB.16          |        :x:         |         |                                                                                   |        :x:         |
| BB.17          |        :x:         |         |                                                                                   |        :x:         |

The table below presents a list of formulas from the Eurocode 3 standards for steel structures, specific to the 
National Annex of the Netherlands.

| Formula number | Done | Remarks | Object name |
|:---------------|:----:|:--------|:------------|
| NB.1           | :x:  |         |             |
| NB.2           | :x:  |         |             |
| NB.3           | :x:  |         |             |
| NB.4           | :x:  |         |             |
| NB.5           | :x:  |         |             |
| NB.6           | :x:  |         |             |
| NB.7           | :x:  |         |             |
| NB.8           | :x:  |         |             |
| NB.9           | :x:  |         |             |
| NB.10          | :x:  |         |             |
| NB.11          | :x:  |         |             |
| NB.12          | :x:  |         |             |
| NB.13          | :x:  |         |             |
| NB.14          | :x:  |         |             |
| NB.15          | :x:  |         |             |
| NB.16          | :x:  |         |             |
| NB.17          | :x:  |         |             |
| NB.18          | :x:  |         |             |
| NB.19          | :x:  |         |             |
| NB.20          | :x:  |         |             |
| NB.21          | :x:  |         |             |
| NB.22          | :x:  |         |             |
| NB.23          | :x:  |         |             |
| NB.24          | :x:  |         |             |
| NB.25          | :x:  |         |             |
| NB.26          | :x:  |         |             |
| NB.27          | :x:  |         |             |
| NB.28          | :x:  |         |             |
| NB.29          | :x:  |         |             |
| NB.30          | :x:  |         |             |
| NB.31          | :x:  |         |             |
| NB.32          | :x:  |         |             |
| NB.33          | :x:  |         |             |
| NB.34          | :x:  |         |             |
| NB.35          | :x:  |         |             |
| NB.36          | :x:  |         |             |
| NB.37          | :x:  |         |             |
| NB.38          | :x:  |         |             |
| NB.39          | :x:  |         |             |
| NB.40          | :x:  |         |             |
| NB.41          | :x:  |         |             |
| NB.42          | :x:  |         |             |
| NB.43          | :x:  |         |             |
| NB.44          | :x:  |         |             |
| NB.45          | :x:  |         |             |
| NB.46          | :x:  |         |             |
| NB.47          | :x:  |         |             |
| NB.48          | :x:  |         |             |
| NB.49          | :x:  |         |             |
| NB.50          | :x:  |         |             |
| NB.51          | :x:  |         |             |
| NB.52          | :x:  |         |             |
| NB.53          | :x:  |         |             |
| NB.54          | :x:  |         |             |
| NB.55          | :x:  |         |             |
| NB.56          | :x:  |         |             |
| NB.57          | :x:  |         |             |
| NB.58          | :x:  |         |             |
| NB.59          | :x:  |         |             |
| NB.60          | :x:  |         |             |
| NB.61          | :x:  |         |             |
| NB.62          | :x:  |         |             |
| NB.63          | :x:  |         |             |
| NB.64          | :x:  |         |             |
| NB.65          | :x:  |         |             |
| NB.66          | :x:  |         |             |
| NB.67          | :x:  |         |             |
| NB.68          | :x:  |         |             |
| NB.69          | :x:  |         |             |
| NB.70          | :x:  |         |             |
| NB.71          | :x:  |         |             |
| NB.72          | :x:  |         |             |
| NB.73          | :x:  |         |             |
| NB.74          | :x:  |         |             |
| NB.75          | :x:  |         |             |
| NB.76          | :x:  |         |             |
| NB.77          | :x:  |         |             |
| NB.78          | :x:  |         |             |
| NB.79          | :x:  |         |             |
| NB.80          | :x:  |         |             |
| NB.81          | :x:  |         |             |
| NB.82          | :x:  |         |             |
| NB.83          | :x:  |         |             |
| NB.84          | :x:  |         |             |
| NB.85          | :x:  |         |             |
| NB.86          | :x:  |         |             |
| NB.BB.1        | :x:  |         |             |
| NB.NA.1        | :x:  |         |             |
| NB.NA.2        | :x:  |         |             |
| NB.NA.3        | :x:  |         |             |
| NB.NA.4        | :x:  |         |             |
| NB.NA.5        | :x:  |         |             |
| NB.NA.6        | :x:  |         |             |
| NB.NA.7        | :x:  |         |             |
| NB.NA.8        | :x:  |         |             |
| NB.NA.9        | :x:  |         |             |
| NB.NA.10       | :x:  |         |             |
| NB.NA.11       | :x:  |         |             |
| NB.NA.12       | :x:  |         |             |
| NB.NA.13       | :x:  |         |             |
| NB.NA.14       | :x:  |         |             |
| NB.NA.15       | :x:  |         |             |
| NB.NA.16       | :x:  |         |             |
| NB.NA.17       | :x:  |         |             |
| NB.NA.18       | :x:  |         |             |
| NB.NA.19       | :x:  |         |             |
| NB.NA.20       | :x:  |         |             |
| NB.NA.21       | :x:  |         |             |
| NB.NA.22       | :x:  |         |             |
| NB.NA.23       | :x:  |         |             |
| NB.NA.24       | :x:  |         |             |
| NB.NA.25       | :x:  |         |             |
| NB.NA.26       | :x:  |         |             |
| NB.NA.27       | :x:  |         |             |
| NB.NA.28       | :x:  |         |             |
| NB.NA.29       | :x:  |         |             |
| NB.NA.30       | :x:  |         |             |
| NB.NA.31       | :x:  |         |             |
| NB.NA.32       | :x:  |         |             |
| NB.NA.33       | :x:  |         |             |
| NB.NA.34       | :x:  |         |             |
| NB.NA.35       | :x:  |         |             |
| NB.NA.36       | :x:  |         |             |
| NB.NA.37       | :x:  |         |             |
| NB.NA.38       | :x:  |         |             |
| NB.NA.39       | :x:  |         |             |
| NB.NA.40       | :x:  |         |             |
| NB.NA.41       | :x:  |         |             |
| NB.NA.42       | :x:  |         |             |
| NB.NA.43       | :x:  |         |             |
| NB.NA.44       | :x:  |         |             |
| NB.NA.45       | :x:  |         |             |
| NB.NA.46       | :x:  |         |             |
| NB.NA.47       | :x:  |         |             |
| NB.NA.48       | :x:  |         |             |
| NB.NA.49       | :x:  |         |             |
| NB.NA.50       | :x:  |         |             |
| NB.NA.51       | :x:  |         |             |
| NB.NA.52       | :x:  |         |             |
| NB.NA.53       | :x:  |         |             |
| NB.NA.54       | :x:  |         |             |
| NB.NA.55       | :x:  |         |             |
| NB.NA.56       | :x:  |         |             |
| NB.NA.57       | :x:  |         |             |
| NB.NA.58       | :x:  |         |             |
| NB.NA.59       | :x:  |         |             |
| NB.NB.1        | :x:  |         |             |
| NB.NB.2        | :x:  |         |             |
| NB.NB.3        | :x:  |         |             |
| NB.NB.4        | :x:  |         |             |
| NB.NB.5        | :x:  |         |             |
| NB.NB.6        | :x:  |         |             |
| NB.NB.7        | :x:  |         |             |
| NB.NB.8        | :x:  |         |             |
| NB.NB.9        | :x:  |         |             |
| NB.NB.10       | :x:  |         |             |
| NB.NB.11       | :x:  |         |             |
| NB.NB.12       | :x:  |         |             |
| NB.NB.13       | :x:  |         |             |
