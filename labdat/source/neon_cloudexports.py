import os
from keys import Raw

def Load(run, check_file=''):
    source = 'Neon'
    folder = f"{run.folder}\\neon_cloudexports"

    path = [
            f'{folder}\\info.json',
            f'{folder}\\scene_camera.json',
            f'{folder}\\imu.csv',
            f'{folder}\\gaze.csv',
            f'{folder}\\3d_eye_states.csv',
            f'{folder}\\fixations.csv',
            f'{folder}\\events.csv',
            f'{folder}\\world_timestamps.csv',
            f'{folder}\\blinks.csv',]
    
    return [Raw({
        'source':   source,
        'path':     p,
        'run_key':  run.key,
    }) for p in path]