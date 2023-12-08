import os,csv,sys
sys.path.append('../..')
import tools,vars

class Load:
    def Trials(run_key):
        trial_path = []
        for dirpath, dirnames, filenames in os.walk(rf'{vars.raw_path}\{run_key}\Pupil'):
            path = [os.path.join(dirpath, file) for file in filenames if file == "annotations.csv"]
            if path:
                trial_path.append(path[0])

        if(trial_path == []):
            # print(f"Empty at: {run_key}")
            return []

        trial_data = []
        with open(trial_path[0],'r',newline='') as trial_csv:
            trial_reader = list(csv.reader(trial_csv,delimiter=' '))
            for index,row in enumerate(trial_reader):
                if(index==0): continue
                if(index%2==1): trial_data += [row[0].split(',')[0:3]]
                else: trial_data[-1] += row[0].split(',')[0:2]
        
        trial_dict = [{
            "key":f"{i}_{t[2]}",
            "start_index":int(t[0]),
            "end_index":int(t[3]),
            "start_time":float(t[1]),
            "end_time":float(t[4]),
            "experiment_key": run_key
            } 
            for i,t in enumerate(trial_data)]

        return trial_dict