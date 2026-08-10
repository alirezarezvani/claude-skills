import sys
import shutil
import os
from pathlib import Path

# Add scripts dir to sys.path to import find_skills
repo_root = Path(r"C:\Users\AHMED\.gemini\config\plugins\claude-skills")
import importlib.util

repo_root = Path(r"C:\Users\AHMED\.gemini\config\plugins\claude-skills")
spec = importlib.util.spec_from_file_location("sync", str(repo_root / "scripts" / "sync-gemini-skills.py"))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
find_skills = sync.find_skills

def main():
    skills = find_skills(repo_root)
    plugin_skills_dir = repo_root / "skills"
    plugin_skills_dir.mkdir(parents=True, exist_ok=True)
    
    for skill in skills:
        skill_name = skill["name"]
        skill_dest_dir = plugin_skills_dir / skill_name
        skill_dest_dir.mkdir(exist_ok=True)
        
        dest_md = skill_dest_dir / "SKILL.md"
        
        # skill["source"] is a relative path like "../../../marketing-skill/seo/SKILL.md"
        # Since it's relative to .gemini/skills/{name}/SKILL.md in the original script,
        # we can reconstruct the absolute path by taking the relative path from repo_root.
        # But wait, find_skills builds it as "../../../" + str(rel_path).
        # We can just extract the rel_path part:
        source_rel_path = skill["source"].replace("../../../", "")
        source_abs_path = repo_root / source_rel_path
        
        try:
            shutil.copy2(source_abs_path, dest_md)
            print(f"Copied {skill_name}")
            
            # Also, if the source was a SKILL.md in a directory, there might be a scripts/ or other resources.
            # We can optionally copy them, but wait, the prompt doesn't say to copy them.
            # If the skill relies on local scripts, a copy of SKILL.md won't have access to them unless we copy the whole directory.
            # Let's copy the entire directory if the source is named SKILL.md, else just copy the file.
            if source_abs_path.name == "SKILL.md":
                source_dir = source_abs_path.parent
                for item in source_dir.iterdir():
                    if item.name != "SKILL.md" and item.name != ".git":
                        dest_item = skill_dest_dir / item.name
                        if item.is_dir():
                            if not dest_item.exists():
                                shutil.copytree(item, dest_item)
                        else:
                            if not dest_item.exists():
                                shutil.copy2(item, dest_item)
        except Exception as e:
            print(f"Error copying {skill_name}: {e}")

if __name__ == "__main__":
    main()
