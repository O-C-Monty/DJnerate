from mutagen.easyid3 import EasyID3
import librosa
import os

def extract_metadata(filepath):
    try:
        audio = EasyID3(filepath)
        return {
            "title": audio.get("title", ["Unknown"])[0],
            "artist": audio.get("artist", ["Unknown"])[0],
        }
    except:
        return {
            "title": os.path.basename(filepath),
            "artist": "Unknown"
        }

def analyze_audio(filepath):
    y, sr = librosa.load(filepath)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    energy = float(librosa.feature.rms(y=y).mean())
    return {
        "bpm": round(tempo),
        "energy": round(energy, 5)
    }

def process_audio_file(filepath):
    meta = extract_metadata(filepath)
    audio = analyze_audio(filepath)
    return {
        "filepath": filepath,
        **meta,
        **audio
    }
