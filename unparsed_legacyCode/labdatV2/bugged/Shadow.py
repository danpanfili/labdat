import os
from keys import Raw
from glob import glob

shadowName = {
    "Gq":   "Global.RotQuat",               # Quaternion
    "Gdq":  "Global.RotQuatDelta",          # Quaternion
    "Lq":   "Local.RotQuat",                # Quaternion
    "r":    "Local.RotEuler",               # Radians
    "la":   "Global.Acc",                   # g
    "lv":   "Global.Vel",                   # cm/sec
    "lt":   "Global.Pos",                   # cm
    "c":    "Global.PositionConstraint",    # cm, unitless weight
    "a":    "Calibrated.Accelerometer",     # g
    "m":    "Calibrated.Magnetometer",      # microtesla
    "g":    "Calibrated.Gyroscope",         # deg/sec
    "A":    "Raw.Accelerometer",            # int16
    "M":    "Raw.Magnetometer",             # int16
    "G":    "Raw.Gyroscope",                # int16
}

def Rename(val: str, key = '.', sn = shadowName):
    name = val.split('.')[-1][:-1]
    if name == '':  return val # Bug fix, prevents weirdness when name is 1 char long
    if name in sn:  return val.replace(name, sn[name])
    else:           return val.replace(name, f'Generic.{name}')

def Load(run, check_file='take*stream.csv'):
    source = 'Shadow'
    folder = f"{run.folder}\\{source}"

    take_path = glob(f"{folder}\\{check_file}")
    if take_path is False: return
    if len(take_path) != 1: return
    take_path = take_path[0]

    path = [
        take_path,
        f"{folder}\\take.mTake",
        f"{folder}\\configuration.mNode"]
    
    path = [p for p in path if os.path.exists(p)]
    
    return [Raw({
        'source':   source,
        'path':     p,
        'run_key':  run.key,
    }) for p in path]