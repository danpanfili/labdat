import os,csv,json
import tools,vars,time,source,experiment

vars.raw_path = r"Z:\rawdata"
vars.out_path = r'Z:\labdat\output'

class Export:
    def CSV(data,name=''):
        headers = [d['key'] for d in data] # Extract headers from the 'key' field in the dictionaries
        rows = list(zip(*[entry['data'] for entry in data])) # Extract values from the 'value' field in the dictionaries

        with open(rf'{vars.out_path}\{name}.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            writer.writerows(rows)
    def Matlab(data,name=''):
        return
    def Numpy():
        return

class Save:
    def Json(save_dict,filename=''):
        with open(f'{vars.out_path}\\{filename}.json', "w") as file: json.dump(save_dict,file)
        return
class Load:
    class Data:
        def Raw(main_dict,run_key,trial_key='',data_key=''):
            raw_data = []

            run_dict,trial_dict,data_dict = zip(*[
                    [d['run'],d['trial'],d['data']] 
                    for d in tools.FindDict(main_dict,{'key':run_key}) 
                    if any(tools.FindDict(d['data'],{'key':data_key}))
                    and any(tools.FindDict(d['trial'],{'key':trial_key}))
                ])
            
            trial_dict = [tools.FindDict(td,{'key':trial_key}) for td in trial_dict]
            data_dict = [tools.FindDict(dd,{'key':data_key}) for dd in data_dict]
            
            startTime = time.time()
            for run,trial,data in zip(run_dict,trial_dict,data_dict):
                for t in trial:
                    for d in data:
                        [data_path,config_path] = [
                            getattr(getattr(source, submodule).Load, 'Path')(run['key']) 
                            for submodule in source.submodules 
                            if tools.Contains(d['key'],submodule) 
                            and hasattr(getattr(source, submodule), 'Load')
                            ][0]
                        # print(f"{run['key']}|{trial['key']}|{data['key']}")
                        raw_data += [{'key':f"{run['key']}|{t['key']}|{d['key']}",'data':tools.GetLineCSV(data_path,t,d)}]
                print(time.time() - startTime)
            return raw_data
        def Dict(main_dict,run_key,trial_key='',data_key=''):
            raw_data = {}

            run_dict,trial_dict,data_dict = zip(*[
                    [d['run'],d['trial'],d['data']] 
                    for d in tools.FindDict(main_dict,{'key':run_key}) 
                    if any(tools.FindDict(d['data'],{'key':data_key}))
                    and any(tools.FindDict(d['trial'],{'key':trial_key}))
                ])
            
            trial_dict = [tools.FindDict(td,{'key':trial_key}) for td in trial_dict]
            data_dict = [tools.FindDict(dd,{'key':data_key}) for dd in data_dict]

            startTime = time.time()
            for r,trial,data in zip(run_dict,trial_dict,data_dict):
                [exp,sub,run] = tools.Key2Array(r['key'],'_')
                for t in trial:
                    [trial_num,trial_type] = tools.Key2Array(t['key'],'_')
                    for d in data:
                        [data_path,config_path] = [
                            getattr(getattr(source, submodule).Load, 'Path')(r['key']) 
                            for submodule in source.submodules 
                            if tools.Contains(d['key'],submodule) 
                            and hasattr(getattr(source, submodule), 'Load')
                            ][0]
                        # print(f"{run['key']}|{trial['key']}|{data['key']}")

                        [src,marker,*dataType] = tools.Key2Array(d['key'],'_')
                        dict_hierarchy = [exp,sub,run,trial_type,trial_num,src,marker]
                        dict_hierarchy += [dt for dt in dataType]
                        raw_data = tools.ConstructNestedDict(dict_hierarchy,raw_data,tools.GetLineCSV(data_path,t,d))
                        #Need to write a batch processor for the getLineCSV, too inefficient

                    #Add trial stuff here
                    raw_data[exp][sub][run][trial_type][trial_num].update({
                        'index':{'start':t['start_index'],'end':t['end_index']},
                        'time':{'start':t['start_time'],'end':t['end_time']}
                    })
                print(time.time() - startTime)
            return raw_data
        
    class Dict:
        def All():
            run_key,source_name = Load.Keys.Run()
            trial_dict = [Load.Keys.Trial(key) for key in run_key]
            data_dict = [Load.Keys.Data(key) for key in run_key]
            run_dict = [{
                "key":key,
                "sources":tools.Array2Key(source,","),
                "numTrials":len(trial),
                "trial_key":tools.Array2Key(tools.FindDict(trial,None,"key"),","),
                "data_key":tools.Array2Key(tools.FindDict(data,None,"key"),",")
            } 
            for key,source,trial,data in zip(run_key,source_name,trial_dict,data_dict)]

            return [{
                "key":run['key'],
                "run":run,
                "trial":trial,
                "data":data} for run,trial,data in zip(run_dict,trial_dict,data_dict)]
        
    class Keys:
        def Run():
            experiment_name = [name for name in os.listdir(vars.raw_path) if os.path.isdir(rf"{vars.raw_path}\{name}")]
            run_key, source_name = [],[]
            run_key = []

            for index,experiment in enumerate(experiment_name):
                experiment_path = rf"{vars.raw_path}\{experiment}"
                
                subject_name = [name for name in os.listdir(experiment_path) if os.path.isdir(rf"{experiment_path}\{name}")]
                if(subject_name == []): continue

                for subject in subject_name:
                    subject_path = rf"{experiment_path}\{subject}"
                    
                    run_name = [name for name in os.listdir(subject_path) if os.path.isdir(rf"{subject_path}\{name}")]
                    if(run_name == []): continue

                    [run_key.append(tools.Array2Key([experiment,subject,run],"_")) for run in run_name]

                    for run in run_name:
                        run_path = rf"{subject_path}\{run}"
                        source_name += [[name for name in os.listdir(run_path) if os.path.isdir(rf"{run_path}\{name}")]]
            return run_key,source_name
        def Trial(run_key):
            if tools.Contains(run_key,"BerkeleyOutdoorWalk"): return experiment.BerkeleyOutdoorWalk.Load.Trials(run_key)
            return []
        def Data(run_key):
            data_dict = []
            if tools.Contains(run_key,"BerkeleyOutdoorWalk"):
                shadow_dict = source.shadow.Load.Keys(run_key)
                if shadow_dict: data_dict += shadow_dict
                
                pupil_dict = source.pupil.Load.Keys(run_key)
                if pupil_dict: data_dict += pupil_dict

            return data_dict
    # class Data:


main_dict = Load.Dict.All()
data_dict = Load.Data.Dict(main_dict,'Subject03','rocks','shadow_Head_')
# data = Load.Data.Raw(main_dict,'Subject03','rocks','shadow_Head_')
# data += Load.Data.Raw(main_dict,'Subject03','rocks','shadow_time_')
# data = sorted(data, key=lambda x: x['key'])
# Export.CSV(data,tools.Array2Key(['Subject03','rocks','shadow_Head_','shadow_time_'],"."))
print("Done!")

#Need to go through an automate the checks for experiment and source, then automatically go to submodule for run based on name. See how this was done in Load.Data with getattr()
#also need to add in interpolation mechanics, treating all data the same currently
#We should also be checking if a database already exists before running, save multiples and can have a flag to redo a section and overwrite