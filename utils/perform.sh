#! /bin/bash 

# rm nohup.out
python3 main.py dev reboot update_all fix_videos export &
python3 main.py main reboot &
