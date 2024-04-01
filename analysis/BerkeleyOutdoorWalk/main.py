import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as Rot
from scipy.signal import savgol_filter
import pandas as pd

class Camera:
    def __init__(self, res, fov):
        self.res = res
        self.fov = fov

        self.deg_per_pix = [f/r for f in fov for r in res]

class L: # Logic
    def AND (a, b): return a & b
    def OR  (a, b): return a | b
    def XOR (a, b): return a ^ b
    def NAND(a, b): return ~(a & b)
    def NOR (a, b): return ~(a | b)
    def XNOR(a, b): return ~(a ^ b)

class Local:
    def __init__(self, arr, width): 
        self.arr    = arr
        self.width  = width
        self.local  = [np.roll(self.arr, i) for i in range(-self.width, self.width+1)]
        self.mean   = np.nanmean(    self.local, axis=0 )
        self.median = np.nanmedian(  self.local, axis=0 )
        self.std    = np.nanstd(     self.local, axis=0 )
        self.min    = np.nanmin(     self.local, axis=0 )
        self.max    = np.nanmax(     self.local, axis=0 )

    def Local(arr, width):    return [np.roll(arr, i) for i in range(-width, width+1)]

    def Mean(arr, width):     return np.nanmean(    Local.Local(arr, width), axis=0 )
    def Median(arr, width):   return np.nanmedian(  Local.Local(arr, width), axis=0 )
    def Std(arr, width):      return np.nanstd(     Local.Local(arr, width), axis=0 )
    def Min(arr, width):      return np.nanmin(     Local.Local(arr, width), axis=0 )
    def Max(arr, width):      return np.nanmax(     Local.Local(arr, width), axis=0 )

def Filter(arr, low=0, high=1): arr[(arr < low) or (arr > high)] = np.nan; return arr

def Smooth(arr, polyorder=3, width=7): return savgol_filter(arr, window_length=width, polyorder=polyorder, axis=0)

def TrimKey(key, cutLast = False):
    key = [k.split('.') for k in key]
    while len(set([k[0] for k in key]))==1: key = [k[1:] for k in key]
    return ['.'.join(k[:-1]) if len(k[-1]) == 1 and cutLast else '.'.join(k) for k in key]

#################################
# The functions below should be vectorized instead of list comprehension, too slow rn
def Extract(sqlGet):        return { k: np.frombuffer(d, dt) for k,d,dt in zip(TrimKey(sqlGet['key']), sqlGet['data'], sqlGet['dtype']) }
def Condense(var):          return { uk: np.squeeze( np.stack( [var[k] for k in var if uk in k], axis=-1 ) ) for uk in np.unique(TrimKey(var.keys(), cutLast= True)) }

def Normalize(arr):         return np.column_stack( [arr[:,i] / np.linalg.norm( arr, axis=1 ) for i in range(arr.shape[1])] )

def Dot     (arr, width=1): return np.einsum( 'ij,ij->i', arr[:-width,:], arr[width:,:] )

def Angle   (arr, width=1): return np.insert( np.arccos( Dot(arr, width) ),                 0, np.zeros(width), axis=0 )
def Axis    (arr, width=1): return np.insert( np.cross(arr[:-1,:], arr[1:,:], axis=1 ),     0, np.zeros([width, arr.shape[1]]), axis=0 )
def Diff    (arr, order=1): return np.insert( np.diff(arr, n=order),                        0, np.zeros(order), axis=0 )
def Grad    (arr, order=1): return np.gradient(arr, axis=0)

def Rad2Deg(data):          return np.multiply(data, 360/(np.pi*2) )
def Deg2Rad(data):          return np.multiply(data, (np.pi*2)/360 )
#################################

class Eye:
    def __init__(self, id, data):
        self.id     = id
        self.data   = data
        self.index  = data['pupil_positions.Frame.Eye'] == id
        self.vec    = data['pupil_positions.Normal'][self.index,:]
        self.time   = data['pupil_positions.Frame.Time'][self.index]

        self.Delta()
        self.Local()

    def Delta(self):
        self.ang    = Angle(self.vec)
        self.axis   = Axis(self.vec)

        self.dt     = Diff(self.time)
        # self.dt[self.dt*120 > 2.5] = 0.00000001

        self.vel    = self.ang          / self.dt
        self.acc    = Grad(self.vel)    / self.dt

    def Local(self, width=3):
        self.l_ang      = Local(self.ang, width).median
        self.l_ang_vel  = self.l_ang            / self.dt
        self.l_ang_acc  = Grad(self.l_ang_vel)  / self.dt

        self.l_vel      = Local(self.vel, width).median
        self.l_vel_acc  = Grad(self.l_vel)      / self.dt

        self.l_acc      = Local(self.acc, width).mean

    def Smooth(self):
        # Change this up to smooth out the vel and acc, then filter the raw data
        self.sm_ang                             = self.ang
        self.sm_ang[Rad2Deg(self.acc) > 150]    = np.nan
        self.sm_ang[Rad2Deg(self.vel) > 300]    = np.nan
        self.sm_ang                             = pd.Series(self.sm_ang).interpolate('linear')
        self.sm_ang                             = Smooth(self.sm_ang)
        self.sm_ang[self.sm_ang < 0] = np.nan
        self.sm_ang[Rad2Deg(self.sm_ang) > 5] = np.nan

        self.sm_vel    = self.sm_ang        / Diff(self.time)
        self.sm_acc    = Diff(self.sm_vel)  / Diff(self.time, 2)

    def Fixations(self): return

    def Rad(self, attr): return getattr(self, attr)
    def Deg(self, attr): return Rad2Deg( getattr(self, attr) )


def Test(db):
    fixation = {
        'vel':  [0, 65],
        'acc':  [0, 65],
        'time': [.1, .5],}

    saccade = {
        'time': [.03, .25],}

    smooth = {
        'method': 'sgolay',
        'order': 4,
        'width': 5
    }

    run = 'BerkeleyOutdoorWalk.Subject03.Binocular'

    data = db(run.split('.')[0], 'C:\\database\\raw').Get(run, order='name', filter=["source='Pupil'", "name GLOB '[^G]*'"], listRows=True)
    data = Condense(Extract(data))
    
    eye = [Eye(i,data) for i in range(2)]

    # for i in range(10): plt.plot(eye[0].time, Local.Min( eye[0].Deg('vel'), i )); plt.ylim(-10, 200); plt.xlim(1600,1620)
    # plt.ylim(-10, 200); plt.xlim(1600,1650); plt.plot(eye[0].time, eye[0].Deg('vel')) ); plt.plot(eye[0].time, eye[0].Deg('l_ang_vel')) ); plt.plot(eye[0].time, eye[0].Deg('l_vel') )
    # plt.ylim(-200, 200); plt.xlim(1600,1610); plt.plot(eye[0].time, eye[0].Deg('l_ang_acc')); plt.plot(eye[0].time, eye[0].Deg('l_vel_acc')); plt.plot(eye[0].time, eye[0].Deg('l_acc'))
    # plt.plot(eye[0].time, np.min([Local.Mean( eye[0].Deg('vel'), i ) for i in range(5)], axis=0) ); plt.ylim(-10, 400); plt.xlim(1580,1630)

    # maxV = 50; depth = 5; plt.plot(eye[0].time, np.sum([Local.Min( eye[0].Deg('vel'), i )/(i+1) > maxV for i in range(depth)], axis=0)); plt.ylim(-1, depth); plt.xlim(1600,1650)

    1

def Plot(eye):
    depth = 10; 
    maxV = 65

    plt.plot(eye[0].time, eye[0].Deg('vel') / maxV); 
    plt.plot(eye[0].time, Local.Median(eye[0].Deg('vel'),2) / maxV); 

    fixChanceMean   = np.sum([(Local.Mean( eye[0].Deg('vel'), i ) < maxV) / depth for i in range(depth)], axis=0)
    fixChanceMedian = np.sum([(Local.Median( eye[0].Deg('vel'), i ) < maxV) / depth for i in range(depth)], axis=0)
    fixChanceMax = np.sum([(Local.Max( eye[0].Deg('vel'), i ) < maxV) / depth for i in range(depth)], axis=0)
    fixChanceMin = np.sum([(Local.Min( eye[0].Deg('vel'), i ) < maxV) / depth for i in range(depth)], axis=0)
                        
    plt.plot(eye[0].time, -fixChanceMean); 
    plt.plot(eye[0].time, -fixChanceMedian); 
    plt.plot(eye[0].time, -fixChanceMax); 
    plt.plot(eye[0].time, -fixChanceMin); 
    plt.ylim(-1.1, 3); 
    plt.xlim(1600,1610); 
    plt.grid(); 
    plt.legend(['Raw Velocity', 'Median Velocity', 'Fixation Chance: Mean Vel', 'Fixation Chance: Median Vel', 'Fixation Chance: Max Vel', 'Fixation Chance: Min Vel'])

print('Done')