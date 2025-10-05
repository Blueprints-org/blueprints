**EN 1992-1-1 - December 2004
Eurocode 2: Design of concrete structures
Part 1-1: General rules and rules for buildings**

The table presents a list of formulas from the Eurocode 2 standards for concrete structures, tracking their implementation status 
( :x: or :heavy_check_mark: ) and any pertinent remarks. The 'Object Name' column references the corresponding Python entities inside of Blueprints.

Total of 304 formulas present.

| Formula number |        Done        | Remarks | Object name                                               |
|:---------------|:------------------:|:--------|:----------------------------------------------------------|
| 3.1            | :heavy_check_mark: |         | Form3Dot1EstimationConcreteCompressiveStrength            |
| 3.2            | :heavy_check_mark: |         | Form3Dot2CoefficientDependentOfConcreteAge                |
| 3.3            | :heavy_check_mark: |         | Form3Dot3AxialTensileStrengthFromTensileSplittingStrength |
| 3.4            | :heavy_check_mark: |         | Form3Dot4DevelopmentTensileStrength                       |
| 3.5            | :heavy_check_mark: |         | Form3Dot5ApproximationVarianceElasticModulusOverTime      |
| 3.6            | :heavy_check_mark: |         | Form3Dot6CreepDeformationOfConcrete                       |
| 3.7            | :heavy_check_mark: |         | Form3Dot7NonLinearCreepCoefficient                        |
| 3.8            | :heavy_check_mark: |         | Form3Dot8TotalShrinkage                                   |
| 3.9            | :heavy_check_mark: |         | Form3Dot9DryingShrinkage                                  |
| 3.10           | :heavy_check_mark: |         | Form3Dot10CoefficientAgeConcreteDryingShrinkage           |
| 3.11           | :heavy_check_mark: |         | Form3Dot11AutogeneShrinkage                               |
| 3.12           | :heavy_check_mark: |         | Form3Dot12AutogeneShrinkageInfinity                       |
| 3.13           | :heavy_check_mark: |         | Form3Dot13CoefficientTimeAutogeneShrinkage                |
| 3.14           | :heavy_check_mark: |         | Form3Dot14StressStrainForShortTermLoading                 |
| 3.15           | :heavy_check_mark: |         | Form3Dot15DesignValueCompressiveStrength                  |
| 3.16           | :heavy_check_mark: |         | Form3Dot16DesignValueTensileStrength                      |
| 3.17           | :heavy_check_mark: |         | Form3Dot17CompressiveStressConcrete                       |
| 3.18           | :heavy_check_mark: |         | Form3Dot18CompressiveStressConcrete                       |
| 3.19           | :heavy_check_mark: |         | Form3Dot19And20EffectivePressureZoneHeight                |
| 3.20           | :heavy_check_mark: |         | Form3Dot19And20EffectivePressureZoneHeight                |
| 3.21           | :heavy_check_mark: |         | Form3Dot21And22EffectiveStrength                          |
| 3.22           | :heavy_check_mark: |         | Form3Dot21And22EffectiveStrength                          |
| 3.23           | :heavy_check_mark: |         | Form3Dot23FlexuralTensileStrength                         |
| 3.24           | :heavy_check_mark: |         | Form3Dot24IncreasedCharacteristicCompressiveStrength      |
| 3.25           | :heavy_check_mark: |         | Form3Dot25IncreasedCharacteristicCompressiveStrength      |
| 3.26           | :heavy_check_mark: |         | Form3Dot26IncreasedStrainAtMaxStrength                    |
| 3.27           | :heavy_check_mark: |         | Form3Dot27IncreasedStrainLimitValue                       |
| 3.28           | :heavy_check_mark: |         | Form3Dot28RatioLossOfPreStressClass1                      |
| 3.29           | :heavy_check_mark: |         | Form3Dot29RatioLossOfPreStressClass2                      |
| 3.30           | :heavy_check_mark: |         | Form3Dot30RatioLossOfPreStressClass3                      |
| 4.1            | :heavy_check_mark: |         | Form4Dot1NominalConcreteCover                             |
| 4.2            | :heavy_check_mark: |         | Form4Dot2MinimumConcreteCover                             |
| 4.3N           | :heavy_check_mark: |         | Form4Dot3nCheckExecutionTolerances                        |
| 4.4N           | :heavy_check_mark: |         | Form4Dot4nCheckExecutionTolerances                        |
| 5.1            | :heavy_check_mark: |         | Form5Dot1Imperfections                                    |
| 5.2            | :heavy_check_mark: |         | Form5Dot2Eccentricity                                     |
| 5.3a           | :heavy_check_mark: |         | Form5Dot3aTransverseForceUnbracedMembers                  |
| 5.3b           | :heavy_check_mark: |         | Form5Dot3bTransverseForceBracedMembers                    |
| 5.4            | :heavy_check_mark: |         | Form5Dot4TransverseForceEffectBracingSystem               |
| 5.5            | :heavy_check_mark: |         | Form5Dot5TransverseForceEffectFloorDiaphragm              |
| 5.6            | :heavy_check_mark: |         | Form5Dot6TransverseForceEffectRoofDiaphragm               |
| 5.7            | :heavy_check_mark: |         | Form5Dot7EffectiveFlangeWidth                             |
| 5.7a           | :heavy_check_mark: |         | Form5Dot7aFlangeEffectiveFlangeWidth                      |
| 5.7b           | :heavy_check_mark: |         | Form5Dot7bFlangeEffectiveFlangeWidth                      |
| 5.8            | :heavy_check_mark: |         | Form5Dot8EffectiveSpan                                    |
| 5.9            | :heavy_check_mark: |         | Form5Dot9DesignSupportMomentReduction                     |
| 5.10a          | :heavy_check_mark: |         | Form5Dot10aRedistributionOfMomentsLowerFck                |
| 5.10b          | :heavy_check_mark: |         | Form5Dot10bRedistributionOfMomentsUpperFck                |
| 5.11N          | :heavy_check_mark: |         | Form5Dot11nShearSlendernessCorrectionFactor               |
| 5.12N          | :heavy_check_mark: |         | Form5Dot12nRatioDistancePointZeroAndMaxMoment             |
| 5.13N          | :heavy_check_mark: |         | Form5Dot13nSlendernessCriterionIsolatedMembers            |
| 5.13a          | :heavy_check_mark: |         | SubForm5Dot13aCreepRatio                                  |
| 5.13b          | :heavy_check_mark: |         | SubForm5Dot13bMechanicalReinforcementFactor               |
| 5.13c          | :heavy_check_mark: |         | SubForm5Dot13cMomentRatio                                 |
| 5.14           | :heavy_check_mark: |         | Form5Dot14SlendernessRatio                                |
| 5.15           | :heavy_check_mark: |         | Form5Dot15EffectiveLengthBraced                           |
| 5.16           | :heavy_check_mark: |         | Form5Dot16EffectiveLengthUnbraced                         |
| 5.17           | :heavy_check_mark: |         | Form5Dot17EffectiveLengthBucklingLoad                     |
| 5.18           | :heavy_check_mark: |         | Form5Dot18ComparisonGeneralSecondOrderEffects             |
| 5.19           | :heavy_check_mark: |         | Form5Dot19EffectiveCreepCoefficient                       |
| 5.20           | :heavy_check_mark: |         | Form5Dot20DesignModulusElasticity                         |
| 5.21           | :heavy_check_mark: |         | Form5Dot21NominalStiffness                                |
| 5.22a          | :heavy_check_mark: |         | Form5Dot22FactorKs                                        |
| 5.22b          | :heavy_check_mark: |         | Form5Dot22FactorKc                                        |
| 5.23           | :heavy_check_mark: |         | Form5Dot23FactorConcreteStrengthClass                     |
| 5.24           | :heavy_check_mark: |         | Form5Dot24AxialForceCorrectionFactor                      |
| 5.25           | :heavy_check_mark: |         | Form5Dot25AxialForceCorrectionFactor                      |
| 5.26a          | :heavy_check_mark: |         | Form5Dot26FactorKs                                        |
| 5.26b          | :heavy_check_mark: |         | Form5Dot26FactorKs                                        |
| 5.27           | :heavy_check_mark: |         | Form5Dot27EffectiveDesignModulusElasticity                |
| 5.28           | :heavy_check_mark: |         | Form5Dot28TotalDesignMoment                               |
| 5.29           | :heavy_check_mark: |         | Form5Dot29BetaFactor                                      |
| 5.30           | :heavy_check_mark: |         | Form5Dot30TotalDesignMoment                               |
| 5.31           | :heavy_check_mark: |         | Form5Dot31DesignMoment                                    |
| 5.32           | :heavy_check_mark: |         | Form5Dot32EquivalentFirstOrderEndMoment                   |
| 5.33           | :heavy_check_mark: |         | Form5Dot33NominalSecondOrderMoment                        |
| 5.34           | :heavy_check_mark: |         | Form5Dot34Curvature                                       |
| 5.35           | :heavy_check_mark: |         | Form5Dot35EffectiveDepth                                  |
| 5.36           | :heavy_check_mark: |         | Form5Dot36RelativeAxialForce                              |
| 5.37           | :heavy_check_mark: |         | Form5Dot37CreepFactor                                     |
| 5.38a          | :heavy_check_mark: |         | Form5Dot38aCheckRelativeSlendernessRatio                  |
| 5.38b          | :heavy_check_mark: |         | Form5Dot38bCheckRelativeEccentricityRatio                 |
| 5.39           | :heavy_check_mark: |         | Form5Dot39SimplifiedCriterionBiaxialBending               |
| 5.40a          | :heavy_check_mark: |         | Form5Dot40aCheckLateralInstability                        |
| 5.40b          | :heavy_check_mark: |         | Form5Dot40bCheckLateralInstability                        |
| 5.41           | :heavy_check_mark: |         | Form5Dot41MaxForceTendon                                  |
| 5.42           | :heavy_check_mark: |         | Form5Dot42ConcreteCompressiveStress                       |
| 5.43           | :heavy_check_mark: |         | Form5Dot43InitialPrestressForce                           |
| 5.44           | :heavy_check_mark: |         | Form5Dot44PrestressLoss                                   |
| 5.45           | :heavy_check_mark: |         | Form5Dot45LossesDueToFriction                             |
| 5.46           | :heavy_check_mark: |         | Form5Dot46TimeDependentLosses                             |
| 5.47           | :heavy_check_mark: |         | Form5Dot47UpperCharacteristicPrestressingValue            |
| 5.48           | :heavy_check_mark: |         | Form5Dot48LowerCharacteristicPrestressingValue            |
| 6.1            | :heavy_check_mark: |         | Form6Dot1DesignShearStrength                              |
| 6.2            | :heavy_check_mark: |         | Form6Dot2ShearResistance                                  |
| 6.3N           | :heavy_check_mark: |         | Form6Dot3nShearCapacityWithoutRebar                       |
| 6.4            | :heavy_check_mark: |         | Form6Dot4ShearResistance                                  |
| 6.5            | :heavy_check_mark: |         | Form6Dot5ShearForceCheck                                  |
| 6.6N           | :heavy_check_mark: |         | Form6Dot6nStrengthReductionFactor                         |
| 6.7N           | :heavy_check_mark: |         | Form6Dot7nCheckCotTheta                                   |
| 6.8            | :heavy_check_mark: |         | Form6Dot8ShearResistance                                  |
| 6.9            | :heavy_check_mark: |         | Form6Dot9MaximumShearResistance                           |
| 6.10.abN       | :heavy_check_mark: |         | Form6Dot10abnStrengthReductionFactor                      |
| 6.11.abcN      | :heavy_check_mark: |         | Form6Dot11abcnCompressionChordCoefficient                 |
| 6.12           | :heavy_check_mark: |         | Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf   |
| 6.13           | :heavy_check_mark: |         | Form6Dot13ShearResistanceInclinedReinforcement            |
| 6.14           | :heavy_check_mark: |         | Form6Dot14MaxShearResistanceInclinedReinforcement         |
| 6.15           | :heavy_check_mark: |         | Form6Dot15ShearReinforcementResistance                    |
| 6.16           | :heavy_check_mark: |         | Form6Dot16NominalWebWidth                                 |
| 6.17           | :heavy_check_mark: |         | Form6Dot17NominalWebWidth                                 |
| 6.18           | :heavy_check_mark: |         | Form6Dot18AdditionalTensileForce                          |
| 6.19           | :heavy_check_mark: |         | Form6Dot19CheckShearForce                                 |
| 6.20           | :heavy_check_mark: |         | Form6Dot20LongitudinalShearStress                         |
| 6.21           | :heavy_check_mark: |         | Form6Dot21CheckTransverseReinforcement                    |
| 6.22           | :heavy_check_mark: |         | Form6Dot22CheckCrushingCompressionStruts                  |
| 6.23           | :heavy_check_mark: |         | Form6Dot23CheckShearStressInterface                       |
| 6.24           | :heavy_check_mark: |         | Form6Dot24DesignShearStress                               |
| 6.25           | :heavy_check_mark: |         | Form6Dot25DesignShearResistance                           |
| 6.26           | :heavy_check_mark: |         | Form6Dot26ShearStressInWall                               |
| 6.27           | :heavy_check_mark: |         | Form6Dot27ShearForceInWall                                |
| 6.28           | :heavy_check_mark: |         | Form6Dot28RequiredCrossSectionalArea                      |
| 6.29           | :heavy_check_mark: |         | Form6Dot29CheckTorsionShearResistance                     |
| 6.30           | :heavy_check_mark: |         | Form6Dot30DesignTorsionalResistanceMoment                 |
| 6.31           | :heavy_check_mark: |         | Form6Dot31CheckTorsionShearResistanceRectangular          |
| 6.32           | :heavy_check_mark: |         | Form6Dot32EffectiveDepthSlab                              |
| 6.33           | :heavy_check_mark: |         | Form6Dot33ContourRadiusCircularColumnHeads                |
| 6.34           | :heavy_check_mark: |         | Form6Dot34And35ContourRadiusRectangular                   |
| 6.35           | :heavy_check_mark: |         | Form6Dot34And35ContourRadiusRectangular                   |
| 6.36           | :heavy_check_mark: |         | Form6Dot36ExternalContourRadiusCircularColumnHeads        |
| 6.37           | :heavy_check_mark: |         | Form6Dot37InternalContourRadiusCircularColumnHeads        |
| 6.38           | :heavy_check_mark: |         | Form6Dot38MaxShearStress                                  |
| 6.39           | :heavy_check_mark: |         | Form6Dot39BetaCoefficient                                 |
| 6.40           |        :x:         |         |                                                           |
| 6.41           | :heavy_check_mark: |         | Form6Dot41W1Rectangular                                   |
| 6.42           | :heavy_check_mark: |         | Form6Dot42BetaCircular                                    |
| 6.43           | :heavy_check_mark: |         | Form6Dot43BetaRectangular                                 |
| 6.44           | :heavy_check_mark: |         | Form6Dot44BetaRectangular                                 |
| 6.45           | :heavy_check_mark: |         | Form6Dot45W1Rectangular                                   |
| 6.46           | :heavy_check_mark: |         | Form6Dot46BetaCorner                                      |
| 6.47           | :heavy_check_mark: |         | Form6Dot47PunchingShearResistance                         |
| 6.47 k         | :heavy_check_mark: |         | SubForm6Dot47FactorK                                      |
| 6.47 rho_l     | :heavy_check_mark: |         | SubForm6Dot47FactorRhoL                                   |
| 6.47 sigma_cp  | :heavy_check_mark: |         | SubForm6Dot47FactorSigmaCp                                |
| 6.47 sigma_cy  | :heavy_check_mark: |         | SubForm6Dot47FactorSigmaCy                                |
| 6.47 sigma_cz  | :heavy_check_mark: |         | SubForm6Dot47FactorSigmaCz                                |
| 6.48           | :heavy_check_mark: |         | Form6Dot48NetAppliedPunchingForce                         |
| 6.49           | :heavy_check_mark: |         | Form6Dot49AppliedPunchingShearStress                      |
| 6.50           | :heavy_check_mark: |         | Form6Dot50PunchingStressResistance                        |
| 6.51           | :heavy_check_mark: |         | Form6Dot51AppliedPunchingShearStressEccentricLoading      |
| 6.52           | :heavy_check_mark: |         | Form6Dot52PunchingShearResistance                         |
| 6.53           | :heavy_check_mark: |         | Form6Dot53CheckPunchingShear                              |
| 6.54           | :heavy_check_mark: |         | Form6Dot54ControlPerimeter                                |
| 6.55           | :heavy_check_mark: |         | Form6Dot55DesignStrengthConcreteStruts                    |
| 6.56           | :heavy_check_mark: |         | Form6Dot56DesignStrengthConcreteStrussTransverseTension   |
| 6.57N          | :heavy_check_mark: |         | Form6Dot57nNuPrime                                        |
| 6.58           | :heavy_check_mark: |         | Form6Dot58And59TensileForce                               |
| 6.59           | :heavy_check_mark: |         | Form6Dot58And59TensileForce                               |
| 6.60           | :heavy_check_mark: |         | Form6Dot60DesignValueCompressiveStressResistance          |
| 6.61           | :heavy_check_mark: |         | Form6Dot61DesignValueCompressiveStressResistance          |
| 6.62           | :heavy_check_mark: |         | Form6Dot62DesignValueCompressiveStressResistance          |
| 6.63           | :heavy_check_mark: |         | Form6Dot63ConcentratedResistanceForce                     |
| 6.64           | :heavy_check_mark: |         | Form6Dot64BondFactor                                      |
| 6.65           | :heavy_check_mark: |         | Form6Dot65ConcreteCompressionStrut                        |
| 6.66           |        :x:         |         |                                                           |
| 6.67           |        :x:         |         |                                                           |
| 6.68           |        :x:         |         |                                                           |
| 6.69           |        :x:         |         |                                                           |
| 6.70           | :heavy_check_mark: |         | Form6Dot70FatigueDamageFactor                             |
| 6.71           | :heavy_check_mark: |         | Form6Dot71CriteriaBasedOnStressRange                      |
| 6.72           | :heavy_check_mark: |         | Form6Dot72FatigueResistanceConcreteCompression            |
| 6.73           | :heavy_check_mark: |         | Form6Dot73StressRatio                                     |
| 6.74           | :heavy_check_mark: |         | Form6Dot74MinimumCompressiveStressLevel                   |
| 6.75           | :heavy_check_mark: |         | Form6Dot75MaximumCompressiveStressLevel                   |
| 6.76           | :heavy_check_mark: |         | Form6Dot76DesignFatigueStrengthConcrete                   |
| 6.77           | :heavy_check_mark: |         | Form6Dot77FatigueVerification                             |
| 6.78           | :heavy_check_mark: |         | Form6Dot78And79FatigueResistance                          |
| 6.79           | :heavy_check_mark: |         | Form6Dot78And79FatigueResistance                          |
| 7.1            | :heavy_check_mark: |         | Form7Dot1MinReinforcingSteel                              |
| 7.2            | :heavy_check_mark: |         | Form7Dot2StressDistributionCoefficient                    |
| 7.2sub1        | :heavy_check_mark: |         | Form7Dot2Sub1AxialForceCoefficient                        |
| 7.3            | :heavy_check_mark: |         | Form7Dot3CoefficientKc                                    |
| 7.4            | :heavy_check_mark: |         | Form7Dot4MeanStressConcrete                               |
| 7.5            | :heavy_check_mark: |         | Form7Dot5AdjustedBondStrengthRatio                        |
| 7.6N           | :heavy_check_mark: |         | Form7Dot6nMaxBarDiameterBending                           |
| 7.7N           | :heavy_check_mark: |         | Form7Dot7nMaxBarDiameterTension                           |
| 7.8            | :heavy_check_mark: |         | Form7Dot8CrackWidth                                       |
| 7.9            | :heavy_check_mark: |         | Form7Dot9EpsilonSmMinusEpsilonCm                          |
| 7.10           | :heavy_check_mark: |         | Form7Dot10RhoPEff                                         |
| 7.11           | :heavy_check_mark: |         | Form7Dot11MaximumCrackSpacing                             |
| 7.12           | :heavy_check_mark: |         | Form7Dot12EquivalentDiameter                              |
| 7.13           | :heavy_check_mark: |         | Form7Dot13CoefficientK2                                   |
| 7.14           | :heavy_check_mark: |         | Form7Dot14MaximumCrackSpacing                             |
| 7.15           | :heavy_check_mark: |         | Form7Dot15MaximumCrackSpacing                             |
| 7.16.a         | :heavy_check_mark: |         | Form7Dot16abSpanDepthRatio                                |
| 7.16.b         | :heavy_check_mark: |         | Form7Dot16abSpanDepthRatio                                |
| 7.17           | :heavy_check_mark: |         | Form7Dot17MultiplicationFactor                            |
| 7.18           | :heavy_check_mark: |         | Form7Dot18DeformationParameter                            |
| 7.19           | :heavy_check_mark: |         | Form7Dot19DistributionCoefficient                         |
| 7.20           | :heavy_check_mark: |         | Form7Dot20EffectiveModulus                                |
| 7.21           | :heavy_check_mark: |         | Form7Dot21CurvatureDueToShrinkage             
| 8.1            | :heavy_check_mark: |         | Form8Dot1RequiredMinimumMandrelDiameter                   |
| 8.2            | :heavy_check_mark: |         | Form8Dot2UltimateBondStress                               |
| 8.3            | :heavy_check_mark: |         | Form8Dot3RequiredAnchorageLength                          |
| 8.4            | :heavy_check_mark: |         | Form8Dot4DesignAnchorageLength                            |
| 8.5            | :heavy_check_mark: |         | Form8Dot5ProductAlphas235                                 |
| 8.6            | :heavy_check_mark: |         | Form8Dot6MinimumTensionAnchorage                          |
| 8.7            | :heavy_check_mark: |         | Form8Dot7MinimumCompressionAnchorage                      |
| 8.8N           | :heavy_check_mark: |         | Form8Dot8nAnchorageCapacityWeldedTransverseBar            |
| 8.9            | :heavy_check_mark: |         | Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiamet  |
| 8.10           | :heavy_check_mark: |         | Form8Dot10DesignLapLength                                 |
| 8.11           | :heavy_check_mark: |         | Form8Dot11MinimumDesignLapLength                          |
| 8.12           | :heavy_check_mark: |         | Form8Dot12AdditionalShearReinforcement                    |
| 8.13           | :heavy_check_mark: |         | Form8Dot13AdditionalShearReinforcement                    |
| 8.14           | :heavy_check_mark: |         | Form8Dot14EquivalentDiameterBundledBars                   |
| 8.15           | :heavy_check_mark: |         | Form8Dot15PrestressTransferStress                         |
| 8.16           | :heavy_check_mark: |         | Form8Dot16BasicTransmissionLength                         |
| 8.17           | :heavy_check_mark: |         | Form8Dot17DesignValueTransmissionLength1                  |
| 8.18           | :heavy_check_mark: |         | Form8Dot18DesignValueTransmissionLength2                  |
| 8.19           | :heavy_check_mark: |         | Form8Dot19DispersionLength                                |
| 8.20           | :heavy_check_mark: |         | Form8Dot20BondStrengthAnchorageULS                        |
| 8.21           | :heavy_check_mark: |         | Form8Dot21AnchorageLength                                 |
| 9.1N           | :heavy_check_mark: |         | Form9Dot1nMinimumTensileReinforcementBeam                 |
| 9.2            | :heavy_check_mark: |         | Form9Dot2ShiftInMomentDiagram                             |
| 9.3            | :heavy_check_mark: |         | Form9Dot3ShiftInMomentDiagram                             |
| 9.4            | :heavy_check_mark: |         | Form9Dot4ShearReinforcementRatio                          |
| 9.5N           | :heavy_check_mark: |         | Form9Dot5nMinimumShearReinforcementRatio                  |
| 9.6N           | :heavy_check_mark: |         | Form9Dot6nMaximumDistanceShearReinforcement               |
| 9.7N           | :heavy_check_mark: |         | Form9Dot7nMaximumDistanceBentUpBars                       |
| 9.8N           | :heavy_check_mark: |         | Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks   |
| 9.9            | :heavy_check_mark: |         | Form9Dot9MaximumSpacingSeriesOfLinks                      |
| 9.10           | :heavy_check_mark: |         | Form9Dot10MaximumSpacingBentUpBars                        |
| 9.11           | :heavy_check_mark: |         | Form9Dot11MinimumShearReinforcement                       |
| 9.12N          | :heavy_check_mark: |         | Form9Dot12nMinimumLongitudinalReinforcementColumns        |
| 9.13           | :heavy_check_mark: |         | Form9Dot13TensileForceToBeAnchored                        |
| 9.14           | :heavy_check_mark: |         | Form9Dot14SplittingForceColumnOnRock                      |
| 9.15           | :heavy_check_mark: |         | Form9Dot15MinimumResistancePeripheralTie                  |
| 9.16           | :heavy_check_mark: |         | Form9Dot16MinimumForceOnInternalBeamLine                  |
| 10.1           |        :x:         |         |                                                           |
| 10.2           |        :x:         |         |                                                           |
| 10.3           |        :x:         |         |                                                           |
| 10.4           |        :x:         |         |                                                           |
| 10.5           |        :x:         |         |                                                           |
| 10.6           |        :x:         |         |                                                           |
| 11.1           |        :x:         |         |                                                           |
| 11.2           |        :x:         |         |                                                           |
| 11.3.15        |        :x:         |         |                                                           |
| 11.3.16        |        :x:         |         |                                                           |
| 11.3.24        |        :x:         |         |                                                           |
| 11.3.26        |        :x:         |         |                                                           |
| 11.3.27        |        :x:         |         |                                                           |
| 11.6.2         |        :x:         |         |                                                           |
| 11.6.5         |        :x:         |         |                                                           |
| 11.6.6N        |        :x:         |         |                                                           |
| 11.6.47        |        :x:         |         |                                                           |
| 11.6.50        |        :x:         |         |                                                           |
| 11.6.52        |        :x:         |         |                                                           |
| 11.6.53        |        :x:         |         |                                                           |
| 11.6.63        |        :x:         |         |                                                           |
| 12.1           | :heavy_check_mark: |         | Form12Dot1PlainConcreteTensileStrength                    |
| 12.2           | :heavy_check_mark: |         | Form12Dot2PlainConcreteBendingResistance                  |
| 12.3           | :heavy_check_mark: |         | Form12Dot3PlainConcreteShearStress                        |
| 12.4           | :heavy_check_mark: |         | Form12Dot4PlainConcreteShearStress                        |
| 12.5           | :heavy_check_mark: |         | Form12Dot5And6PlainConcreteBendingResistance              |
| 12.6           | :heavy_check_mark: |         | Form12Dot5And6PlainConcreteBendingResistance              |
| 12.7           |        :x:         |         |                                                           |
| 12.8           |        :x:         |         |                                                           |
| 12.9           |        :x:         |         |                                                           |
| 12.10          |        :x:         |         |                                                           |
| 12.11          |        :x:         |         |                                                           |
| 12.12          |        :x:         |         |                                                           |
| 12.13          |        :x:         |         |                                                           |
| B.1            |        :x:         |         |                                                           |
| B.2            |        :x:         |         |                                                           |
| B.3a           |        :x:         |         |                                                           |
| B.3b           |        :x:         |         |                                                           |
| B.4            |        :x:         |         |                                                           |
| B.5            |        :x:         |         |                                                           |
| B.6            |        :x:         |         |                                                           |
| B.7            |        :x:         |         |                                                           |
| B.8a           |        :x:         |         |                                                           |
| B.8b           |        :x:         |         |                                                           |
| B.8c           |        :x:         |         |                                                           |
| B.9            |        :x:         |         |                                                           |
| B.10           |        :x:         |         |                                                           |
| B.11           |        :x:         |         |                                                           |
| B.12           |        :x:         |         |                                                           |
| C.1N           |        :x:         |         |                                                           |
| C.2N           |        :x:         |         |                                                           |
| C.3            |        :x:         |         |                                                           |
| D.1            |        :x:         |         |                                                           |
| D.2            |        :x:         |         |                                                           |
| F.1            |        :x:         |         |                                                           |
| F.2            |        :x:         |         |                                                           |
| F.3            |        :x:         |         |                                                           |
| F.4            |        :x:         |         |                                                           |
| F.5            |        :x:         |         |                                                           |
| F.6            |        :x:         |         |                                                           |
| F.7            |        :x:         |         |                                                           |
| F.8            |        :x:         |         |                                                           |
| F.9            |        :x:         |         |                                                           |
| F.10           |        :x:         |         |                                                           |
| G.1            |        :x:         |         |                                                           |
| H.1            |        :x:         |         |                                                           |
| H.2            |        :x:         |         |                                                           |
| H.3            |        :x:         |         |                                                           |
| H.4            |        :x:         |         |                                                           |
| H.5            |        :x:         |         |                                                           |
| H.6            |        :x:         |         |                                                           |
| H.7            |        :x:         |         |                                                           |
| H.8            |        :x:         |         |                                                           |
| I.1            |        :x:         |         |                                                           |
