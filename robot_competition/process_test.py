from main import *

def transTest():
    work=WorkProcess()
    work.transport(work.carry,carryPickImgPoint01,carryPickRecRefer01,carryPickReferPoint01,carryPlaceImgPoint,carryPlaceRecRefer,carryPlaceReferPoint,markerLength,dhCameraMatrix,dhDistCoeffs)

if __name__ == '__main__':
    transTest()