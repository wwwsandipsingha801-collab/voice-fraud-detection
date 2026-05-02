import numpy as np

def predict(mfcc, spec):
    """
    Improved heuristic-based voice classification
    Uses MFCC variance + Spectrogram variance
    """

    # Feature calculations
    mfcc_mean = np.mean(mfcc)
    mfcc_var = np.var(mfcc)
    spec_mean = np.mean(spec)
    spec_var = np.var(spec)

    # Debug prints (very useful)
    print("MFCC mean:", mfcc_mean)
    print("MFCC var:", mfcc_var)
    print("Spec mean:", spec_mean)
    print("Spec var:", spec_var)

    # Decision logic (tuneable thresholds)
    if spec_var < 50 and mfcc_var < 20:
        return "Fake Voice"

    elif spec_var < 80:
        return "Suspicious Voice"

    else:
        return "Real Voice"