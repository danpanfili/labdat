import os,csv,time,sys
sys.path.append('../..')
import tools,vars


class Data:
    def Load(run_key,trial_key,data_key):
        if(tools.Contains(data_key,'gaze')): return Gaze(run_key,trial_key,data_key)
        if(tools.Contains(data_key,'pupil')): return Pupil(run_key,trial_key,data_key)
        if(tools.Contains(data_key,'blink')): return Blink(run_key,trial_key,data_key)
        
    def Gaze(run_key,trial_key,data_key):
        return
    def Pupil(run_key,trial_key,data_key,eye_id=0):
        return
    def Blink(run_key,trial_key,data_key):
        return

class Load:
    def Path(run_key):
        run_path = tools.Key2Path(run_key,'_')

        data_path = f"{vars.raw_path}\{run_path}\\Pupil"
        if os.path.exists(data_path) is False: 
                # print(f"Bad Path, doesn't exist: {data_path}")
                return {'path':'','export_name':''}

        #Check if there are annotations in folder like Berk trial finder for now, people did multiple exports for some reason and that will make this hard
        #This also assumes there is only 1 of these, not robust
        export_name = []
        for dirpath, dirnames, filenames in os.walk(data_path):
            path = [os.path.join(dirpath, file) for file in filenames if file == "annotations.csv"]
            if path:
                export_name.append(path[0].replace("\\annotations.csv","")[-3:])

        if export_name == []: return {'path':'','export_name':''}
        export_name = export_name[0]
        
        return {'path':data_path,'export_name':export_name}

    def Keys(run_key):
        data_path = Load.Path(run_key)
        if data_path['path']=='': return []
        
        gaze_path = rf'{data_path["path"]}\exports\{data_path["export_name"]}\gaze_positions.csv'
        #Making a dict since we need to rename some of the vars, works well
        gaze_marker_list = {
            'timestamp':'time',
            'index':'index',
            'confidence':'confidence',
            'norm_pos_x':'coord_x', 'norm_pos_y':'coord_y',
            'eye_center0_3d_x':'eye0_pos_x', 'eye_center0_3d_x':'eye0_pos_y', 'eye_center0_3d_x':'eye0_pos_z',
            'gaze_normal0_x':'eye0_vec_x', 'gaze_normal0_y':'eye0_vec_y', 'gaze_normal0_z':'eye0_vec_z',
            'eye_center1_3d_x':'eye1_pos_x', 'eye_center1_3d_x':'eye1_pos_y', 'eye_center1_3d_x':'eye1_pos_z',
            'gaze_normal1_x':'eye1_vec_x', 'gaze_normal1_y':'eye1_vec_y', 'gaze_normal1_z':'eye1_vec_z'
        }
        gaze_marker,gaze_index = Load.Subsource(gaze_path,gaze_marker_list)
        gaze_dict = [{
            'key':f'pupil_gaze_{m}',
            'index':gaze_index[i],
            'method':'default',
            'run_key':run_key
        } for i,m in enumerate(gaze_marker)]
            
        pupil_path = rf'{data_path["path"]}\exports\{data_path["export_name"]}\pupil_positions.csv'
        pupil_marker_list = {
            'timestamp':'time',
            'id':'eye',
            'index':'frame_index',
            'confidence':'confidence',
            'theta':'cartesian_elevation',
            'phi':'cartesian_azimuth',
            'norm_pos_x':'coord_x', 'norm_pos_y':'coord_y',
            'eye_3d_center_x':'pos_x', 'circle_3d_center_y':'pos_y', 'circle_3d_center_z':'pos_z',
            'eye_3d_normal_3d_x':'vec_x', 'circle_3d_normal_y':'vec_y', 'circle_3d_normal_z':'vec_z'
        }
        pupil_marker,pupil_index = Load.Subsource(pupil_path,pupil_marker_list)
        pupil_dict = [{
            'key':f'pupil_pupil_{m}',
            'index':pupil_index[i],
            'method':'default',
            'run_key':run_key
        } for i,m in enumerate(pupil_marker)]

        blink_path = rf'{data_path["path"]}\exports\{data_path["export_name"]}\blinks.csv'
        blink_marker_list = {
            'confidence':'confidence',
            'start_timestamp':'time_start',
            'duration':'time_length',
            'end_timestamp':'time_end',
            'start_frame_index':'frame_start',
            'end_frame_index':'frame_end'
        }
        blink_marker,blink_index = Load.Subsource(blink_path,blink_marker_list)
        blink_dict = [{
            'key':f'pupil_blink_{m}',
            'index':blink_index[i],
            'method':'default',
            'run_key':run_key
        } for i,m in enumerate(blink_marker)]

        data_dict = gaze_dict + pupil_dict + blink_dict

        return data_dict
    
    def Subsource(path, marker_list):
        if os.path.exists(path) is False: return [],[]

        with open(path,'r',newline='') as data_csv:
            reader = csv.reader(data_csv,delimiter=',')
            header = reader.__next__()
            [marker,index] = zip(*[[marker_list[h],i] for i,h in enumerate(header) if h in marker_list])
        return marker,index