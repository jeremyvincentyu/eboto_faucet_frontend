from os import listdir,path
import json
#Get a list of all node_modules
all_modules = [every_module for every_module in listdir("node_modules") if every_module[0] != "."]

license_filenames = ["LICENSE","license","COPYING","License","Copying","copying","LICENCE"]
all_licenses: list[tuple[str,str]] = []
replacements: dict[str,list[str]] = {}
unidentified: list[str] = []
#Iterate over every folder in node_modules that do not start with .
for every_folder in all_modules:
    #Identify the module folder
    module_folder = path.join("node_modules",every_folder)
    package_name = every_folder
    
    license_file_read = False
    #Attempt to read the license file directly first
    for every_name in license_filenames:
        license_file_attempt = path.join(module_folder,every_name)
        if path.exists(license_file_attempt):
            
            license_text = ""
            with open(license_file_attempt,"r") as license_file:
                license_text = license_file.read().strip()
            all_licenses.append((package_name,license_text))
            license_file_read = True
            break
    
    if license_file_read:
        continue
    
    license_in_package = False

    #If that doesn't work, extract the license name from package.json, and puth that in place of the license text
    if not license_file_read:
        package_description_path = path.join(module_folder,"package.json")
        if path.exists(package_description_path):
            with open(package_description_path,"r") as package_file:
                package_data = json.loads(package_file.read())
                if "license" in package_data:
                    license_name = package_data["license"]
                    all_licenses.append((package_name,f"REPLACE-WITH-{license_name}"))
                    if license_name not in replacements:
                        replacements[license_name] = []
                    replacements[license_name].append(package_name)
                    license_in_package = True
    if license_in_package:
        continue
    
    #If that still doesn't work, inform me to find the license myself
    if not license_in_package:
        all_licenses.append((package_name,"FIND-MY-LICENSE"))
        unidentified.append(package_name)

#Dump all the license texts into a single file
with open("public/license.txt","w") as combined_file:
    for every_package,every_license in all_licenses:
        combined_file.write("*"*40+"\n")
        combined_file.write(f"The license and/or copyright statement for {every_package} is as follows:\n")
        combined_file.write(f"{every_license}\n")
        combined_file.write("*"*40+"\n")

#Take note of all the identified replacements
with open("replacements.txt","w") as replacement_file:
    replacement_file.write(json.dumps(replacements,indent=4))

#Take note of all the unidentified replacements
with open("unidentified.txt","w") as unidentified_file:
    unidentified_file.write(json.dumps(unidentified,indent=4))