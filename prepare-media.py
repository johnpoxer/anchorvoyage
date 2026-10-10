from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
assets = root / "assets"
assets.mkdir(exist_ok=True)
for filename in ("media-photos.zip", "media-video.zip"):
    with zipfile.ZipFile(root / filename) as archive:
        for member in archive.infolist():
            name = Path(member.filename).name
            if member.is_dir():
                continue
            if member.filename != name or Path(name).suffix.lower() not in {".jpg", ".mp4"}:
                raise ValueError(f"Unexpected media archive entry: {member.filename}")
            (assets / name).write_bytes(archive.read(member))
manifest = json.loads((root / "media-integrity.json").read_text(encoding="utf-8-sig"))
for entry in manifest:
    data = (assets / entry["name"]).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if len(data) != entry["length"] or digest != entry["sha"]:
        raise ValueError(f"Media integrity check failed: {entry['name']}")
print(f"Prepared and verified {len(manifest)} media assets.")
