import os
from google_images_download import google_images_download   #importing the library
from tqdm import tqdm
from argparse import ArgumentParser

IMG_EXTENSIONS = [
    ".jpg",
    ".JPG",
    ".jpeg",
    ".JPEG",
    ".png",
    ".PNG",
    ".ppm",
    ".PPM",
    ".bmp",
    ".BMP",
]

def in_extensions(filename, extensions):
    return any(filename.endswith(extension) for extension in extensions)

def find_image_files(dir, extensions=IMG_EXTENSIONS):
    """
    Get all the images recursively under a dir.
    Args:
        dir:
    Returns: found files, where each item is a tuple (id, ext)
    """
    images = []
    assert os.path.isdir(dir), "%s is not a valid directory" % dir

    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            if in_extensions(fname, extensions):
                path = os.path.join(root, fname)
                images.append(path)
    return images

if __name__ == "__main__":
    parser = ArgumentParser(description="Scrape images given a text file with queries")
    parser.add_argument("--query_list", required=True, help="path to file with queries, one query per line")
    parser.add_argument("--out_dir", required=True, help="path to root output directory. if path doesn't exist, will create")
    parser.add_argument("--num_images_per_query", default=1000, type=int, help="how many images to download per query")
    parser.add_argument("--njobs", type=int, default=1, help="how many parallel scrapers to run")
    parser.add_argument("--resume", action="store_true", help="don't download if already has many images in dir")
    args = parser.parse_args()
    print(args)


    response = google_images_download.googleimagesdownload()   #class instantiation

    queries = [line.strip("\n") for line in open(args.query_list)]
    print("Found", len(queries), "queries.")

    for i, query in enumerate(queries):
        query = query.split("#", 1)[0] # allow comments in file
        
        parts = query.split(",")
        query = parts[0]
        num_groups = max(len(parts[1:]), 1)
        suffix = ",".join(parts[1:])

        folder = query.replace(" ", "_")
        target_dir = os.path.join(args.out_dir, folder)
        os.makedirs(target_dir, exist_ok=True)
        num_previously_found = len(find_image_files(target_dir))

        # get files until thingy
        limit = args.num_images_per_query
        if args.resume:
            do_it = True if num_previously_found < args.num_images_per_query / 2 else False
        else:
            do_it = True
        if limit > 0:
            print(f"===Scraping {limit} images for '{query}'...===")
            arguments = {
                "keywords": query.replace(",", " "),
                "limit": int(limit/num_groups),
                "output_directory": target_dir,
                "chromedriver": "/usr/bin/chromedriver",
                "print_urls": True
            }
            if suffix:
                arguments["suffix_keywords"] = suffix
            response.download(arguments)

