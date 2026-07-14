#!/usr/bin/env python3
"""Build the Dreem Content plugin distributable.

The pack ships as a plugin only (never as standalone .skill files), so the
shared reference files live ONCE at shared/references/ and every skill links
to them via ../../shared/references/_shared-*.md. No copies, no sync step.

Builds dist/dreem-content-plugin.zip: plugin manifest + all skills + shared
references, for one-drop install in Claude Desktop / Cowork.
"""

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
SHARED_REFS = ROOT / "shared" / "references"
DIST = ROOT / "dist"

LINK_RE = re.compile(r"\.\./\.\./shared/references/(_shared-[a-z0-9-]+\.md)")


def check_shared_links() -> None:
    """Every ../../shared/references/ path mentioned in a SKILL.md must exist."""
    missing = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        for fname in set(LINK_RE.findall(skill_md.read_text())):
            if not (SHARED_REFS / fname).exists():
                missing.append(f"{skill_md.parent.name}: {fname}")
    if missing:
        sys.exit("Broken shared-reference links:\n  " + "\n  ".join(missing))


def zip_dir(zf: zipfile.ZipFile, directory: Path, arc_prefix: str) -> int:
    count = 0
    for path in sorted(directory.rglob("*")):
        if path.is_dir() or path.name == ".DS_Store":
            continue
        zf.write(path, f"{arc_prefix}/{path.relative_to(directory)}")
        count += 1
    return count


def build_plugin_zip() -> str:
    out = DIST / "dreem-content-plugin.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(ROOT / ".claude-plugin" / "plugin.json", ".claude-plugin/plugin.json")
        n = 1
        n += zip_dir(zf, SHARED_REFS, "shared/references")
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if (skill_dir / "SKILL.md").exists():
                n += zip_dir(zf, skill_dir, f"skills/{skill_dir.name}")
    return f"{out.name} ({n} files)"


def main() -> None:
    if not SHARED_REFS.exists() or not list(SHARED_REFS.glob("_shared-*.md")):
        sys.exit("No shared reference files found in shared/references/")
    check_shared_links()
    DIST.mkdir(exist_ok=True)
    print(f"Built {build_plugin_zip()}")


if __name__ == "__main__":
    main()
