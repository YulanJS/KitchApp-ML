import os
from tqdm import tqdm
import re
import shutil


def main(root, move_not_copy=False, copy_dir=None, dry_run=False):
    subdirs = next(os.walk(root))[1]
    for dir in tqdm(subdirs):
        dirpath = os.path.join(root, dir)
        for r, _, fs in os.walk(dirpath):
            for name in fs:
                path = os.path.join(r, name)
                new_name = os.path.join(*(path.split(os.path.sep)[3:])).replace(
                    os.path.sep, "."
                )
                new_path = os.path.join(copy_dir, dir, new_name) if copy_dir else os.path.join(dirpath, new_name) 
                new_path = re.sub(r"\s+", "_", new_path, flags=re.UNICODE)
                fname, ext = os.path.splitext(new_path)
                new_path = fname[:139] + ext
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                if dry_run:
                    op = "mov" if move_not_copy else "copy"
                    print(f"(dry) {op}ing {path} to {new_path}")
                else:
                    operation = shutil.move if move_not_copy else shutil.copyfile
                    operation(path, new_path)
            if not dry_run and move_not_copy:
                try:
                    os.rmdir(r)
                except OSError as e:
                    print(e)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("root", help="root folder containing subdirs")
    parser.add_argument("--mode", choices=("copy", "move"), default="copy", help="Whether to copy or move files")
    parser.add_argument("--copydir", help="Where to move copy files")
    parser.add_argument(
        "--dry-run", help="just dry run, don't delete", action="store_true"
    )
    args = parser.parse_args()
    if args.mode == "copy" and not args.copydir:
        print("Must provide copydir if mode is copy")
        exit(1)

    print(
        "This will move collapse all files under the following folders: ",
        sorted(next(os.walk(args.root))[1]),
    )
    if input("Are you sure you want to continue? (y/N): ") == "y":
        main(args.root, args.mode=="move", args.copydir, args.dry_run)
    else:
        print("Did not receive 'y'. Exiting.")
