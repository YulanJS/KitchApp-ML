import argparse
from keras.models import load_model
import coremltools

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("model_file", help="path to .h5 keras model")
parser.add_argument("class_list", help="path to list of classes (1 per line)")
parser.add_argument("--image_scale", default="1.", help="image scale")

args = parser.parse_args()

coreml_model = coremltools.converters.keras.convert(
    args.model_file,
    input_names="image",
    image_input_names="image",
    class_labels=args.class_list,
    image_scale=eval(args.image_scale)
)

output = args.model_file.rsplit(".", 1)[0] + ".mlmodel"
coreml_model.save(output)
