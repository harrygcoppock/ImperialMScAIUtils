'''
This is for the submitting scripts to Imperials gpucluster. You need to be ssh'd into username@gpucluster.doc.ic.ac.uk
'''



import os
import subprocess
import glob

user = ''  # put your username here
type_ = ''  # label the job kinda (all runs will be saved to a director with this name)
description = """""" # provide description of job
venv_path = '' # path to your virtual environment
output_path = f'/vol/bitbucket/{user}/'

if user == '' or type_ == '' or venv_path == '':
    raise ValueError('Please fill in your username and the label for the job.')



#make directories
def mkdir_p(dir, level):
    '''make a directory (dir) if it doesn't exist'''
    if not os.path.exists(dir):
        os.mkdir(dir)


def get_next_case_number(directories):
    if not directories:
        return '001'
    max_case_nr = -float('inf')
    for directory in directories:
        case_nr = int(directory)
        max_case_nr = max(max_case_nr, case_nr)

    next_case_nr = '0' * (3 - len(str(max_case_nr + 1))) + str(max_case_nr + 1)
    return next_case_nr



type_path = output_path + f"{type_}/"
mkdir_p(type_path, 'type')  #create subfolder
sub_directories = next(os.walk(type_path))[1]
case_number = get_next_case_number(sub_directories)
case_path = type_path + f"{case_number}/"
mkdir_p(case_path, 'case')  #create case folder
input_path = case_path + "input/"
mkdir_p(input_path, 'input')  #create case input folder
output_path = case_path + "output/"
mkdir_p(output_path, 'output')  #create case output folder

description_file = os.path.join(input_path, f"{case_number}.txt")
with open(description_file, 'w') as ds:
    ds.write(description)

#Make submission file

job_file = os.path.join(input_path, f"{case_number}.sh")
file_to_run = 'python main.py' # swap main.py with your script
with open(job_file, 'w') as fh:

    fh.writelines("#!/bin/bash\n")
    fh.writelines(f"#SBATCH --job-name=audio.job\n")
    fh.writelines(f"#SBATCH --gres=gpu:1")
    fh.writelines(f"#SBATCH --output={output_path}{case_number}.out\n")
    fh.writelines(f"#SBATCH --error={output_path}{case_number}.err\n")
    fh.writelines("#SBATCH --mail-type=ALL\n")
    fh.writelines(f"#SBATCH --mail-user={user}\n")
    fh.writelines("source /vol/cuda/10.1.105-cudnn7.6.5.32/setup.sh\n"
                  )  # point to correct cuda --> check the torch or tensorflow websites to find correct version of cuda
    fh.writelines("TERM=vt100\n")  # or TERM=xterm
    fh.writelines("/usr/bin/nvidia-smi\n")
    fh.writelines("uptime\n")
    fh.writelines(f"{file_to_run}")

# if you have no preference on type of GPU
subprocess.call(
    f"(. {venv_path}bin/activate && sbatch {job_file})",
    shell=True)

# use -w name_of_gpu to specify type of gpu you want
# use -x name_of_gpu to use any type of gpu just not name_of_gpu
# types of gpu: sicklebill, cloud-vm-40-190, kingfisher
# sicklebill is rubbish but if there is a long queue and your job isnt that intense use that.
