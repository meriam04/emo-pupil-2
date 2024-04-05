from pathlib import Path
import sys
import tensorflow as tf

from models.pupil.train import create_model, get_data

CHECKPOINT_PATH = Path(__file__).parent / "checkpoints/binary-006.ckpt"

if __name__ == "__main__":
    # Disable annoying tensorflow warnings
    tf.get_logger().setLevel('ERROR')

    # fix random seed for reproducibility
    tf.random.set_seed(496)

    window_size = 100
    batch_size = 32

    test_set, classes = get_data(Path(sys.argv[1]), Path(sys.argv[2]) / "test", window_size, batch_size)

    input_shape = (window_size, 1)
    num_classes = len(classes)

    # Create the CNN model
    model = create_model(num_classes, input_shape)
    model.load_weights(CHECKPOINT_PATH)

    # Testing
    model.evaluate(test_set)
