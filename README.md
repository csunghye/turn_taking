# Calculating turn-taking measures in natural conversations

This Python script calculates simple turn-taking measures in natural conversations, such as total and mean speech/pause duration and overlapping speech duration, based on timestamps of transcripts. You will need time-stamped transcripts as a tab-separated file to use this script, and columns in the transcripts need to be in a specific order: ['filename', 'start', 'end', 'text', 'speaker', 'task']. The filename and task columns can be empty, but transcripts still need to have at least 6 columns. An example of a transcript is uploaded in this repository: 

# Packages
- Numpy
- Pandas

# Arguments
- `output_file`: The name of a result file. This is a required argument. 
- `input_folder`: The location of the folder where all transcripts are. This is a required argument.
- `speaker`: The speaker label that you want to analyze. If you want to analyze more than one speaker, you will need to run the script again with a different speaker label. This is a required argument, and make sure the speaker label matched the one that you have in the transcripts
- `filetype`: The file extension of the transcripts (e.g., txt). This is an optional argument, and the default is txt. Please note that the transcripts 
must be tab-separated.

# Citation
- Cho, Sunghye, Meredith Cola, Azia Knox, Maggie Rose Pelella, Alison Russell, Aili Hauptmann, Maxine Covello, Christopher Cieri, Mark Liberman, Robert T. Schultz, Julia Parish-Morris. Sex differences in the temporal dynamics of autistic children's natural conversations. Molecular Autism 14, 13. 
