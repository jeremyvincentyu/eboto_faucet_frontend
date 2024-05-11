import json
with open("public/license.txt", "r") as main_license_file:
    main_license_text = main_license_file.read()

with open("replacements.txt","r") as replacements_file:
    replacement_dict = json.loads(replacements_file.read())

for every_license in replacement_dict:
    with open(f"generic_texts/{every_license}.txt","r") as license_file:
        replacement_text = license_file.read().strip()
    main_license_text = main_license_text.replace(f"REPLACE-WITH-{every_license}",replacement_text)

with open("public/license.txt", "w") as main_license_file:
    main_license_file.write(main_license_text)