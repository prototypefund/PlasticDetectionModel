import io

import numpy as np
import pytest
import rasterio

from src.marinedebrisdetector_mod.checkpoints import CHECKPOINTS
from src.marinedebrisdetector_mod.model.segmentation_model import SegmentationModel

MSE_THRESHOLD = 0.01


@pytest.fixture
def input_data():
    with open(
        "tests/data/2400_1440.tiff",
        "rb",
    ) as f:
        return f.read()


@pytest.fixture
def np_data(input_data):
    with rasterio.open(io.BytesIO(input_data)) as src:
        image = src.read()
        meta = src.meta.copy()
        return src, image, meta


@pytest.fixture
def model():
    detector = SegmentationModel.load_from_checkpoint(
        checkpoint_path=CHECKPOINTS["unet++1"],
        strict=False,
        map_location="cpu",
    )
    return detector.to("cpu").eval()


@pytest.fixture
def expected_prediction():
    with open(
        "tests/data/exp_2400_1440_prediction.tiff",
        "rb",
    ) as f:
        return f.read()


@pytest.fixture
def expected_y_score():
    with open(
        "tests/data/exp_y_score.npy",
        "rb",
    ) as f:
        return np.load(f).squeeze()
