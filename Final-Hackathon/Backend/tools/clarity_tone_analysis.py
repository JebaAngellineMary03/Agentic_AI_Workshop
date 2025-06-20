from langchain_core.tools import tool
from llms.llms import llm
from typing import Dict
import os

@tool
def clarity_tone_analysis_tool(transcript: str, audio_path: str, audio_features: Dict) -> str:
    """Analyze speech clarity and tone with audio processing"""
    try:
        from pydub import AudioSegment
        import librosa
        import numpy as np

        audio = AudioSegment.from_file(audio_path)
        duration_seconds = len(audio) / 1000.0
        loudness = audio.dBFS

        y, sr = librosa.load(audio_path)

        try:
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        except:
            tempo = 0.0

        try:
            pitch_array = librosa.yin(y, fmin=80, fmax=450, sr=sr)
            valid_pitch = pitch_array[np.isfinite(pitch_array)]
            pitch_mean = float(np.mean(valid_pitch)) if len(valid_pitch) else 0.0
            pitch_std = float(np.std(valid_pitch)) if len(valid_pitch) else 0.0
        except:
            pitch_mean = pitch_std = 0.0

        try:
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            rms = librosa.feature.rms(y=y)[0]

            zcr_mean = float(np.mean(zcr))
            spectral_centroid_mean = float(np.mean(spectral_centroid))
            rms_mean = float(np.mean(rms))
        except:
            zcr_mean = spectral_centroid_mean = rms_mean = 0.0

        audio_feat_summary = f"""
        Duration: {duration_seconds:.2f} seconds
        Loudness: {loudness:.2f} dB
        Tempo: {tempo:.2f} BPM
        Pitch Mean: {pitch_mean:.2f} Hz
        Pitch Variation: {pitch_std:.2f} Hz
        ZCR: {zcr_mean:.4f}
        Spectral Centroid: {spectral_centroid_mean:.2f} Hz
        RMS Energy: {rms_mean:.4f}
        Channels: {audio_features.get('channels', 'Unknown')}
        Sample Rate: {audio_features.get('sample_rate', 'Unknown')} Hz
        """

        prompt = f"""
        Analyze the following transcript and audio features for:
        1. Clarity Score (0-100)
        2. Tone Score (0-100)
        3. Specific feedback for both
        4. Recommendations to improve

        --- Transcript ---
        {transcript}

        --- Audio Features ---
        {audio_feat_summary}
        """

        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)

    except Exception as e:
        fallback = f"""
        Analyze the following transcript for clarity and tone:

        --- Transcript ---
        {transcript}

        (Note: Audio processing failed.)

        Provide:
        - Clarity Score (0-100)
        - Tone Score (0-100)
        - Feedback and Suggestions
        """

        response = llm.invoke(fallback)
        return response.content if hasattr(response, 'content') else str(response)
