"""Build a reproducible legacy Blender addon ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
output = root / "dist/libsaturn_toolkit.zip"
output.parent.mkdir(exist_ok=True)
with ZipFile(output, "w") as archive:
    for path in sorted((root / "libsaturn_toolkit").glob("*.py")):
        info = ZipInfo(path.relative_to(root).as_posix(), (1980, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())
print(output)
