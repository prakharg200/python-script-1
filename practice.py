import sys
import os
import shutil
import json
from subprocess import run,PIPE

def run_go_files(path):
    code_file_name = None
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith(".go"):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return
    
    result = run(["go","build",code_file_name],stdin=PIPE,stdout=PIPE, universal_newlines=True)
    print("Result- ",result)


def main():
    if len(sys.argv) != 3:
        print("Enter 2 parameters in the console - only")

    #getting source and target dirs from console
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]


    #retrieving paths of directory with "game" in them from the source
    game_dirs = []
    target_game_dirs=[]
    for root,dirs,files in os.walk(source_dir):
        for directory in dirs:
            if "game" in directory.lower():
                game_dirs.append(os.path.join(root,directory))
                new_dir = os.path.join(root,directory).lower().replace("game","")
                _, new_path = os.path.split(new_dir)
                target_game_dirs.append(new_path)
        break
    

    #copying the retrieved dirs from the source to the target with word "game" omitted
    for source_path,target_path in zip(game_dirs,target_game_dirs):
        shutil.copytree(source_path, os.path.join(target_dir,target_path), dirs_exist_ok=True)

    
    #creating a json metadata file for the data info obtained
    data = {
        "numberOfGames": len(game_dirs),
        "nameofGames": game_dirs
    }
    json_file = os.path.join(target_dir,"metadata.json")
    with open(json_file, "w") as f:
        json.dump(data,f)

    #compile and run go files
    for target_path in target_game_dirs:
        run_go_files(os.path.join(target_dir,target_path))

if __name__ == "__main__":
    main()