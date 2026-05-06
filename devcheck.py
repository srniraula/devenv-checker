import subprocess
import argparse
import re
import json
import datetime
import os

INSTALL_INSTRUCTIONS = {
    'docker': 'sudo apt install docker.io',
    'git': 'sudo apt install git',
    'kubectl': 'snap install kubectl --classic',
    'terraform': 'snap install terraform',
    'ansible': 'sudo apt install ansible'
}
tools = ['Docker', 'Git','kubectl','Terraform','Ansible']


def check_tool():
    outputList,uninstalledTools = [],[]
    for tool in tools:
        command = [tool.lower(), '--version']
        try:
            output = subprocess.run(command, capture_output=True, text=True)
            if (output.stderr == ''):
                    match = re.search(r'\d+\.\d+(\.\d+)*',output.stdout)
                    if match:
                        versionResult=match.group()
                    else:
                        versionResult = "version not found"
                    
                    outputList.append({
                        'name': tool,
                        'status': 'OK',
                        'version':versionResult
                    })
            else:
                outputList.append({
                    'name': tool,
                    'status': 'ERROR',
                    'version':'corrupt version'
                })
                uninstalledTools.append(tool)
        except FileNotFoundError:
            outputList.append({
                    'name': tool,
                    'status': 'MISSING',
                    'version':'Not installed'
                })
            uninstalledTools.append(tool)
    return outputList, uninstalledTools

outputList, uninstalledTools = check_tool()
    

parser = argparse.ArgumentParser()
parser.add_argument('--fix', action='store_true', help='Apply fixes')
parser.add_argument('--report', action='store_true', help='Generate report of checks')
args = parser.parse_args()

print("Checking your DevOps Environment....\n")
if args.fix:
    print(f"{len(uninstalledTools)} {"issues" if len(uninstalledTools)>1 else "issue"} found.")
    for tool in uninstalledTools:
        print(INSTALL_INSTRUCTIONS.get(tool.lower(),f"See official docs for {tool}"))
else:
    for item in outputList:
        print("[{0}]   {1}      {2}".format(item['status'],item['name'],item['version']))
    print(f"{len(uninstalledTools)} {"issues" if len(uninstalledTools)>1 else "issue"} found. Run with --fix to see install instructions.")

if args.report:
    report_dict={}
    for itemInfo in outputList:
        report_dict[itemInfo['name']] = {
            'status': itemInfo['status'],
            'version': itemInfo['version']
        }
    report_dict['generated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('report.json', 'w') as f:
        json.dump(report_dict,f,indent=4)

    print(f"Report saved at {os.path.abspath('report.json')}")

