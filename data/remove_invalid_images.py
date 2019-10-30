import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser(argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("root_dir", help="root directory with images")
parser.add_argument("--dry-run", action="store_true", help="just print files to remove without removing")
parser.add_argument("--no_confirm", action="store_true", help="Skip confirmation before deleting")

args = parser.parse_args()

to_delete = []

IMG_EXTENSIONS = [ '.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP', ]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


for root, _, files in os.walk(args.root_dir):
    for name in files:
        if is_image_file(name):
            path = os.path.join(root, name)
            try:
                im = Image.open(path)
                im.verify()
            except (IOError, SyntaxError) as e:
                print("Invalid:", path)
                to_delete.append(path)

print(len(to_delete), "bad files.")
if len(to_delete) > 0 and not args.dry_run:
    a = ""
    while a.lower() != "y" and a.lower() != "n":
        a = input(f"{len(to_delete)} invalid files found to delete. Do you wish to delete? (y/n): ")
    if a.lower() == "y":
        [os.remove(f) for f in to_delete]
        print("Removed all invalid files.")
    else:
        print("No files removed.")

print("Done")
