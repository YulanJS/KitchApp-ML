import os
import shutil


def main(root, dry_run=False):
    subdirs = next(os.walk(root))[1]
    for dir in subdirs:
        dirpath = os.path.join(root, dir)
        for r, _, fs in os.walk(dirpath):
            for name in fs:
                path = os.path.join(r, name)
                new_name = os.path.join(*(path.split(os.path.sep)[2:])).replace(
                    os.path.sep, "."
                )
                new_path = os.path.join(dirpath, new_name)
                if dry_run:
                    print(f"(dry) moving {path} to {new_path}")
                else:
                    shutil.move(path, new_path)
            os.rmdir(r)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("root", help="root folder containing subdirs")
    parser.add_argument(
        "--dry-run", help="just dry run, don't delete", action="store_true"
    )
    args = parser.parse_args()
    print(
        "This will move collapse all files under the following folders: ",
        next(os.walk(args.root))[1],
    )
    if input("Are you sure you want to continue? (y/N): ") == "y":
        main(args.root, args.dry_run)
    else:
        print("Did not receive 'y'. Exiting.")
