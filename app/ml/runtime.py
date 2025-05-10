from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.calibration import CalibratedClassifierCV

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"

clf_path = MODELS_DIR / "diabetes_xgb_calibrated.joblib"
thr_path = MODELS_DIR / "opt_threshold.npy"

try:
    clf: CalibratedClassifierCV = joblib.load(clf_path)

    if isinstance(clf, CalibratedClassifierCV):
        clf._estimator_type = "classifier"

    THRESHOLD: float = float(np.load(thr_path))
except Exception:
    logger.exception("❌ Failed to load model or threshold")
    raise

logger.info(f"✅ Model loaded. Threshold={THRESHOLD:.4f}")


def predict_diabetes(record: Dict[str, Any]) -> Dict[str, Any]:
    df = pd.DataFrame([record])
    p = clf.predict_proba(df)[0, 1]
    return {
        "probability": round(float(p), 4),
        "prediction": int(p > THRESHOLD),
        "threshold": round(float(THRESHOLD), 4),
    }
