import os
import mkdocs_gen_files

# Path to your Python files
src_dir = "src"

# Loop through files in directory
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            full_path = os.path.join(root, file)
            module_path = os.path.relpath(full_path, src_dir)
            module_name = module_path.replace(os.sep, ".").replace(".py", "")
            output_path = os.path.join("reference", f"{module_name}.md")

            with mkdocs_gen_files.open(output_path, "w") as f:
                f.write(f"::: {module_name}\n")

            mkdocs_gen_files.set_edit_path(output_path, full_path)
            print(f"Processing module: {module_name}")
