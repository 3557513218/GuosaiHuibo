from pathlib import Path

import sys
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
from main import *
import config
def armtest():
    work=WorkProcess()
    work.pick(config.agvPointAtCar,config.pickPoints01,config.pickPoints02,config.pickPoints03,config.pickPoints04)
if __name__ == '__main__':
    armtest()