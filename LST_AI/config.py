import os

LST_DATA_DIR = os.environ.get('LST_DATA_DIR', os.path.dirname(__file__))
ATLAS_DIR = os.path.join(LST_DATA_DIR, 'atlas')
MODELS_DIR = os.path.join(LST_DATA_DIR, 'model')
BINARIES_DIR = os.path.join(LST_DATA_DIR, 'binaries')
