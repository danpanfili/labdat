import os
from keys import Raw

newname = {
    'pupil_positions':{
        'index':                'Frame.index',
        'timestamp':            'Frame.time',
        'confidence':           'Frame.confidence',
        'id':                   'Frame.eye',
        'norm_pos_':            'PixelNormal.',
        'ellipse_center_':      'EllipseCenter.',
        'ellipse_axis_':        'EllipseAxis.',
        'sphere_center_':       'SphereCenter.',
        'circle_3d_center_':    'Position.',
        'circle_3d_normal_':    'Normal.',
        'theta':                'Polar.theta',
        'phi':                  'Polar.phi',
    },
    
    'gaze_positions':{
        'index':                'Frame.index',
        'timestamp':            'Frame.time',
        'confidence':           'Frame.confidence',
        'norm_pos_':            'PixelNormal.',
        'eye_center0_':         'LeftEye.Pos.',
        'eye_center1_':         'RightEye.Pos.',
        'eye_normal0_':         'LeftEye.Norm.',
        'eye_normal1_':         'RightEye.Norm.',
    }
}

with open(path,'r') as file:
    line = file.read

def Rename(val: str, key: str, newname = newname):
    file = key.split('.')[-1]
    name = val.split('.')[-1]

    if file not in newname.keys(): return val.replace(name, f'Generic.{name}')

    if name == '':                  return val # Bug fix, prevents weirdness when name is 1 char long
    if name[:-1] in newname[file]:  return val.replace(name[:-1], newname[file][name[:-1]])
    if name in newname[file]:       return val.replace(name, newname[file][name])
    else:                           return val.replace(name, f'Generic.{name}')

def Load(run, check_file='annotations.csv'):
    source = 'Pupil'
    folder = f"{run.folder}\\{source}"

    export_folder = [d[0] for d in os.walk(run.folder) if check_file in d[2]]
    if len(export_folder) != 1: return
    export_folder = export_folder[0]

    path = [f'{folder}\\world.mp4',
            f'{folder}\\eye0.mp4',
            f'{folder}\\eye1.mp4',
            f'{folder}\\world.instrinsics',
            f'{folder}\\world_timestamps.npy',
            f'{export_folder}\\pupil_positions.csv',
            f'{export_folder}\\gaze_positions.csv',
            f'{export_folder}\\export_info.csv',
            f'{export_folder}\\blinks.csv',]
    
    return [Raw({
        'source':   source,
        'path':     p,
        'run_key':  run.key,
    }) for p in path]