import numpy as np

from blueprints.utils.femlearn.mesh import Mesh


class Solution:
    def __init__(
        self,
        mesh=Mesh(),
        meshDeformed=Mesh(),
        dispX=[],
        dispY=[],
        dispTotal=[],
        strainX=[],
        strainY=[],
        strainXY=[],
        stressX=[],
        stressY=[],
        stressXY=[],
        stress11=[],
        stress22=[],
        stress33=[],
        stressMises=[],
        stressZ=[],
    ):
        """
        Contains all the solution variables of the model
        """

        self.mesh = mesh
        self.meshDeformed = meshDeformed
        self.dispX = dispX
        self.dispY = dispY
        self.dispTotal = dispTotal
        self.strainX = strainX
        self.strainY = strainY
        self.strainXY = strainXY
        self.stressX = stressX
        self.stressY = stressY
        self.stressXY = stressXY
        self.stress11 = stress11
        self.stress22 = stress22
        self.stress33 = stress33
        self.stressMises = stressMises
        self.stressZ = stressZ

        # Complete the variables dictionary
        self.variables = {
            "dispX": self.dispX,
            "dispY": self.dispY,
            "dispTotal": self.dispTotal,
            "strainX": self.strainX,
            "strainY": self.strainY,
            "strainXY": self.strainXY,
            "stressX": self.stressX,
            "stressY": self.stressY,
            "stressXY": self.stressXY,
            "stress11": self.stress11,
            "stress22": self.stress22,
            "stress33": self.stress33,
            "stressMises": self.stressMises,
            "stressZ": self.stressZ,
        }

    def _getAveragedResult(self, variableName):
        variable = self.variables[variableName]
        averagedResult = np.zeros([self.mesh.numberOfElements, 1], dtype=np.float64)

        for elementIndex, pointIds in enumerate(self.mesh.elements.integrationpointIds):
            pointIndex = self.mesh.integrationPoints.findIndexByNodeIds(pointIds)
            averagedResult[elementIndex] = np.mean(variable[pointIndex])

        return averagedResult
