"""fstudent_dataset dataset."""

import tensorflow as tf
import tensorflow_datasets as tfds

tfds.load('fstudent_dataset')

_DESCRIPTION = """"""

class FstudentDataset(tfds.core.GeneratorBasedBuilder):

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = \
  {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(fstudent_dataset): Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(None, None, 3)),
            'label': tfds.features.ClassLabel(names=['no', 'yes']),
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=('image', 'label'),  # Set to `None` to disable
        homepage='https://dataset-homepage/',
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(fstudent_dataset): Downloads the data and defines the splits
    path = dl_manager.download_and_extract('https://todo-data-url')

    # TODO(fstudent_dataset): Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(path / 'train_imgs'),
    }

  def _generate_examples(self, path):
    """Yields examples."""
    # TODO(fstudent_dataset): Yields (key, example) tuples from the dataset
    for f in path.glob('*.jpeg'):
      yield 'key', {
          'image': f,
          'label': 'yes',
      }