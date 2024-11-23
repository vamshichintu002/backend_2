import os

old_name = "reference file.py"
new_name = "reference_file.py"

try:
    os.rename(old_name, new_name)
    print(f"Successfully renamed {old_name} to {new_name}")
except Exception as e:
    print(f"Error renaming file: {str(e)}")
