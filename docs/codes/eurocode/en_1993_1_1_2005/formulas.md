**EN 1993-1-1 - May 2005
Eurocode 3: Design of steel structures  
Part 1-1: General rules and rules for buildings**

The table presents a list of formulas from the Eurocode 3 standards for steel structures, tracking their implementation
status (:x: or :heavy_check_mark:)
and any pertinent remarks. The 'Object Name' column references the corresponding Python entities inside of Blueprints.

Total of 108 formulas present.

| Formula number |        Done        | Remarks | Object name                                                                       |
|:---------------|:------------------:|:--------|:----------------------------------------------------------------------------------|
| 2.1            |        :x:         |         |                                                                                   |
| 2.2            | :heavy_check_mark: |         | Form2Dot2CharacteristicValueResistance                                            |
| 5.1            |        :x:         |         |                                                                                   |
| 5.2            |        :x:         |         |                                                                                   |
| 5.3            |        :x:         |         |                                                                                   |
| 5.4            |        :x:         |         |                                                                                   |
| 5.5            |        :x:         |         |                                                                                   |
| 5.6            |        :x:         |         |                                                                                   |
| 5.7            | :heavy_check_mark: |         | Form5Dot7DisregardFrameSwayImperfections                                          |
| 5.8            | :heavy_check_mark: |         | Form5Dot8CheckSlenderness                                                         |
| 5.9            |        :x:         |         |                                                                                   |
| 5.10           |        :x:         |         |                                                                                   |
| 5.11           |        :x:         |         |                                                                                   |
| 5.12           |        :x:         |         |                                                                                   |
| 5.13           |        :x:         |         |                                                                                   |
| 5.14           |        :x:         |         |                                                                                   |
| 6.1            | :heavy_check_mark: |         | Form6Dot1ElasticVerification                                                      |
| 6.2            | :heavy_check_mark: |         | Form6Dot2UtilizationRatio                                                         |
| 6.3            | :heavy_check_mark: |         | Form6Dot3MinDeductionAreaStaggeredFastenerHoles                                   |
| 6.4            | :heavy_check_mark: |         | Form6Dot4AdditionalMoment                                                         |
| 6.5            | :heavy_check_mark: |         | Form6Dot5UnityCheckTensileStrength                                                |
| 6.6            | :heavy_check_mark: |         | Form6Dot6DesignPlasticRestistanceGrossCrossSection                                |
| 6.7            | :heavy_check_mark: |         | Form6Dot7DesignUltimateResistanceNetCrossSection                                  |
| 6.8            | :heavy_check_mark: |         | Form6Dot8NetDesignTensionResistance                                               |
| 6.9            | :heavy_check_mark: |         | Form6Dot9CheckCompressionForce                                                    |
| 6.10           | :heavy_check_mark: |         | Form6Dot10NcRdClass1And2And3                                                      |
| 6.11           | :heavy_check_mark: |         | Form6Dot11NcRdClass4                                                              |
| 6.12           | :heavy_check_mark: |         | Form6Dot12CheckBendingMoment                                                      |
| 6.13           | :heavy_check_mark: |         | Form6Dot13MCRdClass1And2                                                          |
| 6.14           | :heavy_check_mark: |         | Form6Dot14MCRdClass3                                                              |
| 6.15           | :heavy_check_mark: |         | Form6Dot15McRdClass4                                                              |
| 6.16           | :heavy_check_mark: |         | Form6Dot16CheckFlangeWithFastenerHoles                                            |
| 6.17           | :heavy_check_mark: |         | Form6Dot17CheckShearForce                                                         |
| 6.18           | :heavy_check_mark: |         | Form6Dot18DesignPlasticShearResistance                                            |
| 6.18 A_v       | :heavy_check_mark: |         | Various equations                                                                 |
| 6.19           | :heavy_check_mark: |         | Form6Dot19CheckDesignElasticShearResistance                                       |
| 6.20           | :heavy_check_mark: |         | Form6Dot20ShearStress                                                             |
| 6.21           | :heavy_check_mark: |         | Form6Dot21ShearStressIOrHSection                                                  |
| 6.22           | :heavy_check_mark: |         | Form6Dot22CheckShearBucklingResistance                                            |
| 6.23           | :heavy_check_mark: |         | Form6Dot23CheckTorsionalMoment                                                    |
| 6.24           | :heavy_check_mark: |         | Form6Dot24TotalTorsionalMoment                                                    |
| 6.25           | :heavy_check_mark: |         | Form6Dot25CheckCombinedShearForceAndTorsionalMoment                               |
| 6.26           | :heavy_check_mark: |         | Form6Dot26VplTRdIOrHSection                                                       |
| 6.27           | :heavy_check_mark: |         | Form6Dot27VplTRdChannelSection                                                    |
| 6.28           | :heavy_check_mark: |         | Form6Dot28VplTRdHollowSection                                                     |
| 6.29           | :heavy_check_mark: |         | Form6Dot29ReducedYieldStrength                                                    |
| 6.29 (rho)     | :heavy_check_mark: |         | Form6Dot29Rho and Form6Dot29RhoWithTorsion                                        |
| 6.30           | :heavy_check_mark: |         | Form6Dot30ReducedPlasticResistanceMoment                                          |
| 6.31           | :heavy_check_mark: |         | Form6Dot31CheckBendingAndAxialForce                                               |
| 6.32           | :heavy_check_mark: |         | Form6Dot32MNrdRectangular                                                         |
| 6.33           | :heavy_check_mark: |         | Form6Dot33CheckAxialForceY                                                        |
| 6.34           | :heavy_check_mark: |         | Form6Dot34CheckAxialForceY                                                        |
| 6.35           | :heavy_check_mark: |         | Form6Dot35CheckAxialForceZ                                                        |
| 6.36           | :heavy_check_mark: |         | Form6Dot36MomentReduction                                                         |
| 6.37           | :heavy_check_mark: |         | Form6Dot37And38MomentReduction                                                    |
| 6.38           | :heavy_check_mark: |         | Form6Dot37And38MomentReduction                                                    |
| 6.38n          | :heavy_check_mark: |         | Form6Dot38N                                                                       |
| 6.38a          | :heavy_check_mark: |         | Form6Dot38A                                                                       |
| 6.39           | :heavy_check_mark: |         | Form6Dot39ReducedBendingMomentResistance                                          |
| 6.39 a_w       | :heavy_check_mark: |         | Form6Dot39awHollowSections and Form6Dot39awWeldedBoxSections                      |
| 6.40           | :heavy_check_mark: |         | Form6Dot40ReducedBendingMomentResistance                                          |
| 6.40 a_f       | :heavy_check_mark: |         | Form6Dot40afHollowSections and Form6Dot40afWeldedBoxSections                      |
| 6.41           | :heavy_check_mark: |         | Form6Dot41BiaxialBendingCheck                                                     |
| 6.42           |        :x:         |         |                                                                                   |
| 6.43           |        :x:         |         |                                                                                   |
| 6.44           |        :x:         |         |                                                                                   |
| 6.45           |        :x:         |         |                                                                                   |
| 6.46           |        :x:         |         |                                                                                   |
| 6.47           |        :x:         |         |                                                                                   |
| 6.48           |        :x:         |         |                                                                                   |
| 6.49           |        :x:         |         |                                                                                   |
| 6.50           |        :x:         |         |                                                                                   |
| 6.51           |        :x:         |         |                                                                                   |
| 6.52           |        :x:         |         |                                                                                   |
| 6.53           |        :x:         |         |                                                                                   |
| 6.54           |        :x:         |         |                                                                                   |
| 6.55           |        :x:         |         |                                                                                   |
| 6.56           |        :x:         |         |                                                                                   |
| 6.57           |        :x:         |         |                                                                                   |
| 6.58           |        :x:         |         |                                                                                   |
| 6.59           |        :x:         |         |                                                                                   |
| 6.60           |        :x:         |         |                                                                                   |
| 6.61           |        :x:         |         |                                                                                   |
| 6.62           |        :x:         |         |                                                                                   |
| 6.63           |        :x:         |         |                                                                                   |
| 6.64           |        :x:         |         |                                                                                   |
| 6.65           |        :x:         |         |                                                                                   |
| 6.66           |        :x:         |         |                                                                                   |
| 6.67           |        :x:         |         |                                                                                   |
| 6.68           |        :x:         |         |                                                                                   |
| 6.69           |        :x:         |         |                                                                                   |
| 6.70           |        :x:         |         |                                                                                   |
| 6.71           | :heavy_check_mark: |         | FormADot2CriteriaBasedOnStressRangeLHS and FormADot2CriteriaBasedOnStressRangeRHS |
| 6.72           |        :x:         |         |                                                                                   |
| 6.73           |        :x:         |         |                                                                                   |
| 6.74           |        :x:         |         |                                                                                   |
| 6.75           |        :x:         |         |                                                                                   |
| BB.1           |        :x:         |         |                                                                                   |
| BB.2           |        :x:         |         |                                                                                   |
| BB.3           |        :x:         |         |                                                                                   |
| BB.4           |        :x:         |         |                                                                                   |
| BB.5           |        :x:         |         |                                                                                   |
| BB.6           |        :x:         |         |                                                                                   |
| BB.7           |        :x:         |         |                                                                                   |
| BB.8           |        :x:         |         |                                                                                   |
| BB.9           |        :x:         |         |                                                                                   |
| BB.10          |        :x:         |         |                                                                                   |
| BB.11          |        :x:         |         |                                                                                   |
| BB.12          |        :x:         |         |                                                                                   |
| BB.13          |        :x:         |         |                                                                                   |
| BB.14          |        :x:         |         |                                                                                   |
| BB.15          |        :x:         |         |                                                                                   |
| BB.16          |        :x:         |         |                                                                                   |
| BB.17          |        :x:         |         |                                                                                   |