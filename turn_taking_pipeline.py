import glob, argparse, sys, platform
import pandas as pd
import numpy as np

def main(args):

    # check the OS of a user
    user_os = platform.system()
    # assign path separator (backslash or forward-slash depending on the os of the user)
    if user_os == "Windows":
        file_separator = '\\'
    else:
        file_separator = '/'

    # check the file list in the inpuf folder
    if args.filetype:
        list_of_trans = glob.glob(args.input_folder+file_separator+'*.'+args.filetype)
    else:
        list_of_trans = glob.glob(args.input_folder+file_separator+'*.txt')

    # initiate the results dataframe
    SADdf = pd.DataFrame()

    # loop through the filelist
    for transfile in list_of_trans:
	print(transfile, " is being processed.")
        # read one file from the list and assign column names
        df = pd.read_csv(transfile, sep='\t')
        if len(df.columns) == 6:
            df.columns = ['Audio', 'Beg', 'End', 'Text', 'Speaker', 'Section']
        elif len(df.columns) == 7:
            df.columns = ['Kit', 'Audio', 'Beg', 'End', 'Text', 'Speaker', 'Section']
        else:
            sys.exit('The transcript file is not in the right format. Please check again.')  

        # calculate duration of each speech segment
        df['dur'] = df['End'] - df['Beg']

        # calculate duration of pause between speech segments
        df['pause_new_end'] = df['End'].shift(1)
        df['prev_speaker'] = df['Speaker'].shift(1)
        df['prev_pause'] = df['Beg'] - df['pause_new_end']
	
        
        # calculate overlapping speech measures
        overlap_being_sum = abs(df[(df.prev_pause < -0.1) & (df.prev_speaker == args.speaker)]['prev_pause'].sum())
        overlap_being_count = len(df.loc[(df.prev_pause < -0.1) & (df.prev_speaker == args.speaker), 'prev_pause'])
        overlap_being_mean = abs(df[(df.prev_pause < -0.1) & (df.prev_speaker == args.speaker)]['prev_pause'].mean())
	
        overlap_doing_sum = abs(df[(df.prev_pause < -0.1) & (df['Speaker'] == args.speaker)]['prev_pause'].sum())
        overlap_doing_count = len(df.loc[(df.prev_pause < -0.1) & (df['Speaker'] == args.speaker), 'prev_pause'])
        overlap_doing_mean = abs(df[(df.prev_pause < -0.1) & (df['Speaker'] == args.speaker)]['prev_pause'].mean())
        
        overlap_sum = abs(df[df.prev_pause < -0.1]['prev_pause'].sum())
        overlap_count = len(df[df.prev_pause < -0.1]['prev_pause'])
        overlap_mean = abs(df[df.prev_pause < -0.1]['prev_pause'].mean())

        # reset the overlap speech duration to calculate pause duration
        df.loc[df.prev_pause < 0,'prev_pause'] = 0
        # get the task start and end time
        task_start = df['Beg'].min()
        task_end = df['End'].max()

        # get the speech duration measures
        total_dur = df[df['Speaker']==args.speaker]['prev_pause'].agg([np.sum])+ df[df['Speaker']==args.speaker]['dur'].agg([np.sum])
        totalSpch = df[df['Speaker']==args.speaker]['dur'].sum()
        meanSpch = df[df['Speaker']==args.speaker]['dur'].mean()
        sdSpch = df[df['Speaker']==args.speaker]['dur'].std()
        numSpch = len(df[df['Speaker']==args.speaker]['dur'])
        
        # get the between-turn pause duration (i.e., latency to respond) measures
        totalBTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']!=args.speaker)]['prev_pause'].sum()
        meanBTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']!=args.speaker)]['prev_pause'].mean()
        sdBTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']!=args.speaker)]['prev_pause'].std()
        numBTPause = len(df[(df['Speaker']==args.speaker) & (df['prev_speaker']!=args.speaker)]['prev_pause'])

        # get the within-turn pause duration measures
        totalWTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']==args.speaker)]['prev_pause'].sum()
        meanWTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']==args.speaker)]['prev_pause'].mean()
        sdWTpause = df[(df['Speaker']==args.speaker) & (df['prev_speaker']==args.speaker)]['prev_pause'].std()
        numWTPause = len(df[(df['Speaker']==args.speaker) & (df['prev_speaker']==args.speaker)]['prev_pause'])
        
        # stack all results in the temporary dataframe
        temp = pd.DataFrame(pd.np.column_stack([total_dur, totalSpch, meanSpch, sdSpch, numSpch, totalBTpause, meanBTpause, sdBTpause, totalWTpause, meanWTpause, sdWTpause, numBTPause, numWTPause, overlap_sum, overlap_count, overlap_mean, overlap_being_sum, overlap_being_count, overlap_being_mean,overlap_doing_sum, overlap_doing_count, overlap_doing_mean]))
        temp.columns = ['total_dur', 'totalSpch', 'meanSpch','stdSpch', 'numSpch','totalBTPause', 'meanBTPause','stdBTPause','totalWTPause', 'meanWTPause','stdWTPause','numBTPause', 'numWTPause', 'overlap_dur', 'overlap_count', 'overlap_mean','overlap_being_sum', 'overlap_being_count', 'overlap_being_mean','overlap_doing_sum', 'overlap_doing_count', 'overlap_doing_mean']
        temp['filename'] = transfile
        temp['task_start'] = task_start
        temp['task_new_end'] = task_end
		
        # concat the temporary dataframe with the final result dataframe
        SADdf = pd.concat([SADdf, temp])

    # write the final outputs
    SADdf.to_csv(args.output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-output_file', type=str, required=True, help='Name the output file')
    parser.add_argument('-input_folder', type=str, required=True, help='Folder containing input transcript files')
    parser.add_argument('-speaker', type=str, required=True, help='Speaker to be analyzed')
    parser.add_argument('-filetype', type=str, required=False, help='File extension of transcripts')
    args = parser.parse_args()
    main(args)
