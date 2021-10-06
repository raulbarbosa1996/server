import librosa as lb
import numpy as np


# FEATURES
def chroma_feature(audio, sr):
    # Using STFT
    ##Energy (magnitude) Spectrum
    chroma_stft = lb.feature.chroma_stft(y=audio, sr=sr, n_chroma=12, n_fft=4096, hop_length=1024)

    # Chroma Features using CQT
    chroma_cqt = lb.feature.chroma_cqt(y=audio, sr=sr, hop_length=1024)

    return (0.8 * chroma_cqt) + (0.2 * chroma_stft)


def mfcc_features(audio, sr):
    mfcc = lb.feature.mfcc(y=audio, sr=sr, n_mfcc=32, hop_length=1024, htk=True)

    return mfcc


def rms_features(audio):
    S, phase = lb.magphase(lb.stft(audio))
    rms = lb.feature.rms(S=S)
    return rms


def spectral_centroid_features(audio, sr):
    sc = lb.feature.spectral_centroid(y=audio, sr=sr)
    return sc


def spectral_contrast_features(audio, sr):
    S = np.abs(lb.stft(audio))
    sc = lb.feature.spectral_contrast(S=S, sr=sr)
    return sc


def spectral_rolloff_features(audio, sr):
    S, phase = lb.magphase(lb.stft(audio))
    sr = lb.feature.spectral_rolloff(S=S, sr=sr)
    return sr


def zero_crossing_rate_features(audio):
    zcr = lb.feature.zero_crossing_rate(audio)
    return zcr
