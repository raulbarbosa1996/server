import librosa
import numpy as np
import pandas as pd

from utils.feature_extraction import chroma_feature, mfcc_features, rms_features, spectral_rolloff_features, \
    spectral_centroid_features, spectral_contrast_features, zero_crossing_rate_features


def pcm2float(sig, dtype='float32'):
    """Convert PCM signal to floating point with a range from -1 to 1.
    Use dtype='float32' for single precision.
    Parameters
    ----------
    sig : array_like
        Input array, must have integral type.
    dtype : data type, optional
        Desired (floating point) data type.
    Returns
    -------
    numpy.ndarray
        Normalized floating point data.
    See Also
    --------
    float2pcm, dtype
    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be a floating point type")

    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig.astype(dtype) - offset) / abs_max


def audio_to_features(audio, sr):
    audio, index = librosa.effects.trim(audio,top_db=20)
    feature = []

    chroma_features = np.mean(chroma_feature(audio, sr).T, axis=0)
    for i in range(0, len(chroma_features)):
        feature.append(chroma_features[i])

    mfcc = np.mean(mfcc_features(audio, sr).T, axis=0)
    for i in range(0, len(mfcc)):
        feature.append(mfcc[i])

    rms = np.mean(rms_features(audio))
    feature.append(rms)

    spectral_centroid = np.mean(spectral_centroid_features(audio, sr))
    feature.append(spectral_centroid)

    spectral_contrast = np.mean(spectral_contrast_features(audio, sr).T, axis=0)
    for i in range(0, len(spectral_contrast)):
        feature.append(spectral_contrast[i])

    spectral_rolloff = np.mean(spectral_rolloff_features(audio, sr))
    feature.append(spectral_rolloff)

    zero_crossing_rate = np.mean(zero_crossing_rate_features(audio))
    feature.append(zero_crossing_rate)

    return pd.Series(feature)


def scalling_data(data,scaler):
    data_scaled = scaler.transform(data.T)
    data = pd.DataFrame(data_scaled, columns=data.T.columns)
    return data


def predict_classe(model, data):
    score = model.predict(data)
    return np.argmax(score, axis=1),score[0][np.argmax(score, axis=1)]
