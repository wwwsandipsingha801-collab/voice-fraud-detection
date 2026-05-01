import numpy as np

def predict(mfcc, spec):
    """
    Simple dummy model:
    mfcc ka mean nikal ke decide karta hai
    """

    score = np.mean(mfcc)

    # threshold based decision
    if score > -50:
        return "Real Voice"
    else:
        return "Fake Voice"