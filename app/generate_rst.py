import os

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory where RST files will be created (app/docs/source)
docs_source_path = os.path.join(script_dir, 'docs', 'source')

# Create the directory if it doesn't exist
os.makedirs(docs_source_path, exist_ok=True)

# Template for each RST file without dynamic underline
rst_template = """{title}

{underline}

.. automodule:: {module}
    :members:
    :undoc-members:
    :show-inheritance:
"""

# List of modules to generate RST files for
modules = ['app', 'customers', 'inventory', 'reviews', 'sales', 'models']

# Create RST files for each module
for module in modules:
    title = f"{module} Module"
    underline = '=' * len(title)
    rst_content = rst_template.format(title=title, underline=underline, module=module)
    rst_file_path = os.path.join(docs_source_path, f"{module}.rst")
    with open(rst_file_path, 'w') as rst_file:
        rst_file.write(rst_content)
    print(f"Created {rst_file_path}")