import re
import os

def count_submodules():
    count = 0
    if os.path.exists('.gitmodules'):
        with open('.gitmodules', 'r') as f:
            content = f.read()
            count = len(re.findall(r'\[submodule', content))
    return count

def update_readme(submodule_count):
    if not os.path.exists('README.md'):
        return
    
    with open('README.md', 'r') as f:
        readme = f.read()
    
    badge_markdown = f"![Submodules Tracked](https://img.shields.io/badge/Submodules_Tracked-{submodule_count}-blue)"
    
    # Try to replace existing badge
    if '![Submodules Tracked]' in readme:
        readme = re.sub(r'!\[Submodules Tracked\]\(https://img\.shields\.io/badge/Submodules_Tracked-\d+-blue\)', badge_markdown, readme)
    else:
        # Insert after the main title
        readme = re.sub(r'(# [^\n]+\n)', r'\1\n' + badge_markdown + '\n', readme, count=1)
    
    with open('README.md', 'w') as f:
        f.write(readme)

if __name__ == '__main__':
    count = count_submodules()
    print(f"Found {count} submodules. Updating README.md...")
    update_readme(count)
