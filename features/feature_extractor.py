import librosa
import numpy as np

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=16000)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    spec = np.abs(librosa.stft(y))

    mfcc = np.mean(mfcc.T, axis=0)
    spec = np.mean(spec, axis=1)

    return mfcc, spec


if __name__ == "__main__":
    file = "../data/sample/sample.wav"
    mfcc, spec = extract_features(file)

    print("MFCC shape:", mfcc.shape)
    print("Spectrogram shape:", spec.shape)