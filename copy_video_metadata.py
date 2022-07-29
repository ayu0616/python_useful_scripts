import subprocess
from my_helper import get_file_path, MyList
import os

to_file = input("copy to => ").strip()
if not to_file:
    raise TypeError("input filepath")
from_file = get_file_path(os.path.dirname(to_file), filetypes=[("movie files", ("*.mov", "*.mp4", "*.webm", "*.ts"))])

FFMPEG = "/opt/homebrew/bin/ffmpeg"

# get metadata
metadata_filename = os.path.join(os.path.dirname(__file__), "metadata.txt")
try:
    os.remove(metadata_filename)
finally:
    subprocess.run(f"{FFMPEG} -i '{from_file}' -f ffmetadata '{metadata_filename}'", shell=True)

# write metadata
to_file_split_by_dot = to_file.split(".")
written_metadata_filename = os.path.join(os.path.dirname(__file__), "written_metadata." + to_file_split_by_dot[-1])
subprocess.run(
    f"{FFMPEG} -i '{to_file}' -i '{metadata_filename}' -map_metadata 1 -codec copy '{written_metadata_filename}'",
    shell=True,
)

# remove temporary file
os.remove(metadata_filename)
os.rename(written_metadata_filename, to_file)
