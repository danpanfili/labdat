import os,csv,time,sys
sys.path.append('../..')
import tools,vars

class Load:
    def Path(run_key):
        data_path, config_path = [],[]
        
        path = f"{vars.raw_path}\{tools.Key2Path(run_key,'_')}\\Shadow"
        if os.path.exists(path) is False: 
                print(f"Bad Path, doesn't exist: {path}")
                return data_path,config_path
        
        data_file = [file for file in os.listdir(f"{path}") if file.endswith("stream.csv") and file.startswith("take")]
        if data_file == []: return data_path,config_path

        config_path = f"{path}\\configuration.mNode"

        if not os.path.exists(config_path):
            print(f"Bad Path, no config file: {config_path}")
            return data_path,config_path

        data_path = f"{path}\\{data_file[0]}"
        return data_path,config_path

    def Keys(run_key):
        data_path,config_path = Load.Path(run_key)
        if data_path==[]: return []
        
        # config_data = []
        # with open(config_path,'r',newline='') as config_file:
        #     config_data = xmltodict.parse(config_file.read())

        with open(data_path,'r',newline='') as data_csv:
            data_reader = csv.reader(data_csv,delimiter=',')
            data_header = data_reader.__next__()
            
            [data_marker, data_type] = tools.Key2Array(data_header,".")
            
            if 'ltx' not in data_type: #ltx is Linear Translation X, not in some subjects but think they are the unused sample ones
                print("Bad Subject, no Linear Translation Data")
                return []

            data_key, data_index = [],[]
            data_key += ["shadow_time_time","shadow_time_systemtime"]
            data_index += [tools.FindIndex(data_header,".time")[0],tools.FindIndex(data_header,".systemtime")[0]]

            pos_data = [[dh.replace('lt', 'pos_'),index] for index, dh in enumerate(data_header) if 'lt' in dh] #lt* is lateral translation, position
            rot_data = [[dh.replace('Gq', 'rot_'),index] for index, dh in enumerate(data_header) if 'Gq' in dh] #Gq* is global quaternion, rotation
                
            pos_rot_data = sorted(pos_data+rot_data)
            pos_rot_key, pos_rot_index = zip(*pos_rot_data)

            data_key += [f"shadow_{tools.Key2Array(key,'.')[0]}_{tools.Key2Array(key,'.')[1]}" for key in pos_rot_key]
            data_index += pos_rot_index

            data_dict = [{
                "key":key,
                "index":index,
                "method":"default",
                "experiment_key": run_key
                } 
                for key,index in zip(data_key,data_index)]

            return data_dict