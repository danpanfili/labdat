# Move Karl Meshes and PupilShadowMesh
import os, shutil
from glob import glob

path = r'Z:\KarlBackup\data_drive'

def CopyMesh(path = path):
    need_these  = [fr"{path}\allMeshes\s*\texturedMesh.obj",
                fr"{path}\allMeshes\s*\texturedMesh.mtl",
                fr"{path}\allMeshes\s*\texture_*.png",
                fr"{path}\allTraj\s*\cameras.sfm"]

    obj_path    = [glob(nt) for nt in need_these]
    path = []
    for op in obj_path: path += op

    name_trial_file  = [p.split('\\')[-2].split('_')[:-1] + [p.split('\\')[-1]] for p in path]
    new_path    = [fr"Z:\preprocData\BerkeleyOutdoorWalk\Subject{int(nt[0].removeprefix('s')):02d}\KarlMesh\Trial{int(nt[1])}\{nt[2]}" for nt in name_trial_file]

    for p, np in zip(path, new_path): 
        newdir = os.path.dirname(np)
        if not os.path.exists(newdir): os.makedirs(newdir)
        print(f'Copying {p} to {np}...')
        if os.path.exists(np): continue
        shutil.copy(p, np)

def CopyPSM(path = path):
    need_these  = [fr"{path}\pupilShadowMesh\s*pupilShadowMesh.mat"]

    obj_path    = [glob(nt) for nt in need_these]
    path = []
    for op in obj_path: path += op

    name_trial_file  = [p.split('\\')[-1].split('_')[:-1] for p in path]
    new_path    = [fr"Z:\preprocData\BerkeleyOutdoorWalk\Subject{int(nt[0].removeprefix('s')):02d}\PupilShadowMesh\Trial{int(nt[1])}\psm.mat" for nt in name_trial_file]

    for p, np in zip(path, new_path): 
        newdir = os.path.dirname(np)
        if not os.path.exists(newdir): os.makedirs(newdir)
        print(f'Copying {p} to {np}...')
        if os.path.exists(np): continue
        shutil.copy(p, np)

CopyPSM()

print("Done!")