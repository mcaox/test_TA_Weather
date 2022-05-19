from pathlib import Path
import joblib
MODEL_PATH = Path(__file__).parent / "model.joblib"

class ModelGetter:
    MODEL = None
    @classmethod
    def get(cls):
        if cls.MODEL is None:
            import sys
            import xgboost
            from test_TA_Weather.assets.tools import DeltaPressTransformer,DateTransformer
            setattr(sys.modules["__main__"],"DeltaPressTransformer",DeltaPressTransformer)
            setattr(sys.modules["__main__"],"DateTransformer",DateTransformer)
            cls.MODEL = joblib.load(MODEL_PATH)
        return cls.MODEL
