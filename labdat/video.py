import os, cv2, time

class Video():
    ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg'

    def __init__(self, path: str):
        self.path = path
        self.size = os.stat(self.path).st_size
        self.compressed = False

    def Load(self):
        if self.size > (1024**3) and not self.compressed:
            self.Compress()

        with open(self.path, 'rb') as file: return file.read()
    
    def Compress(self, ffmpeg_path = ffmpeg_path): 
        ffmpeg_function = f"{ffmpeg_path} -y -hwaccel auto -i {self.path} -c:v hevc_nvenc -profile main -preset slow -fps_mode vfr -cq:v 19 -rc:v vbr -c:a copy {self.path.replace('.','_c.')}"
        try: os.system(ffmpeg_function)
        except Exception as e: print(f"FFMPEG Error: {e}\n\n")

        self.path       = self.path.replace('.','_c.')
        self.size       = os.stat(self.path).st_size
        self.compressed = True

    def Test(self):
        old = cv2.VideoCapture(self.path);      new = cv2.VideoCapture(self.path.replace('.','_c.'))
        old.set(cv2.CAP_PROP_POS_MSEC,300000);  new.set(cv2.CAP_PROP_POS_MSEC,300000)
        res, oldimg = old.read();               res2, newimg = new.read()
        while res:
            cv2.imshow("Old", oldimg);          cv2.imshow("New", newimg);      cv2.imshow("Diff", cv2.absdiff(oldimg,newimg))
            k = cv2.waitKey(1);                 time.sleep(1/30)
            if k % 256 == 27: break # Press Esc to Close
            res, oldimg = old.read();           res2, newimg = new.read()

# path = r'Z:\rawdata\BerkeleyOutdoorWalk\Subject03\Binocular\Pupil\eye0.mp4'
# vid = Video(path)
# vid.Compress()
# vid.Test()