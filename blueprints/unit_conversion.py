"""Module for unit conversions inside of Blueprints."""

import math

# <editor-fold desc="Forces conversion">
KN_TO_N = 1e3
N_TO_KN = 1e-3
MM3_TO_M3 = 1e-9
MPA_TO_KPA = 1e3
GPA_TO_MPA = 1e3
# </editor-fold>

# <editor-fold desc="Section modulus conversion">
CM3_TO_MM3 = 1e3
# </editor-fold>

# <editor-fold desc="Moments conversion">
NMM_TO_KNM = 1e-6
# </editor-fold>

# <editor-fold desc="Area conversion">
MM2_TO_M2 = 1e-6
# </editor-fold>

# <editor-fold desc="Rotation conversion">
RAD_TO_MRAD = 1e3
MRAD_TO_RAD = 1e-3
RAD_TO_DEG = 180 / math.pi
DEG_TO_RAD = math.pi / 180
# </editor-fold>


# <editor-fold desc="Length conversion">
M_TO_MM = 1e3
MM_TO_M = 1e-3
