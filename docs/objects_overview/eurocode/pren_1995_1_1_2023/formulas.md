# Formulas from prEN 1995-1-1:2023

## Chapter 11 - Fasteners

### 11.2.2.3 Withdrawal resistance

| Formula | Class Name | Description |
|---------|------------|-------------|
| 11.2.2.3-1 | `Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew` | Withdrawal capacity of screws |
| 11.2.2.3-2 | `Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent` | Withdrawal strength dependent on density |
| 11.2.2.3-3 | `Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance` | Design withdrawal resistance |

### Formula Details

#### 11.2.2.3-1: Withdrawal capacity of screws

**Class**: `Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew`

**Description**: Calculates the withdrawal capacity of screws based on the effective head diameter, embedment depth, and withdrawal strength.

**Formula**: F_{w,Rd} = π × d_{head,ef} × l_{ef} × f_{w,k}

**Parameters**:
- `d_head_ef` (MM): Effective head diameter of the screw
- `l_ef` (MM): Effective embedment depth of the screw
- `rho_k` (float): Characteristic density of timber (kg/m³)
- `f_w_k` (MPA): Characteristic withdrawal strength

**Returns**: KN

#### 11.2.2.3-2: Withdrawal strength dependent on density

**Class**: `Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent`

**Description**: Calculates the withdrawal strength of fasteners based on timber density.

**Formula**: f_{w,k} = 20 × (ρ_k/350)^0.8 × d^{-0.2}

**Parameters**:
- `rho_k` (float): Characteristic density of timber (kg/m³)
- `d` (MM): Diameter of the fastener

**Returns**: MPA

#### 11.2.2.3-3: Design withdrawal resistance

**Class**: `Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance`

**Description**: Calculates the design withdrawal resistance considering partial factors.

**Formula**: F_{w,Rd} = (k_{mod} × F_{w,Rk}) / γ_M

**Parameters**:
- `f_w_rk` (KN): Characteristic withdrawal resistance
- `k_mod` (DIMENSIONLESS): Modification factor for load duration and moisture content
- `gamma_m` (DIMENSIONLESS): Partial factor for material properties

**Returns**: KN