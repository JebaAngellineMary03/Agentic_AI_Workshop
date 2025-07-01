from langchain_core.tools import tool
from llms.llms import llm
from typing import Dict
import os

@tool
def clarity_tone_analysis_tool(transcript: str, audio_path: str, audio_features: Dict) -> str:
    """Analyze speech clarity and tone with audio processing based on defined criteria"""
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

        # Define clarity and tone criteria based on extracted features
        clarity_score = 100
        tone_score = 100

        # Clarity Criteria
        if loudness < -30:
            clarity_score -= 20  # Too low loudness
        elif loudness > -5:
            clarity_score -= 10  # Too high loudness
        
        if tempo > 150 or tempo < 90:
            clarity_score -= 15  # Too fast or too slow tempo
        
        if pitch_mean < 80 or pitch_mean > 250:
            clarity_score -= 15  # Pitch out of ideal range
        
        if pitch_std < 0.5:
            clarity_score -= 10  # Low pitch variation
        
        # Tone Criteria
        if pitch_mean < 100 or pitch_mean > 250:
            tone_score -= 10  # Pitch too low or too high
        
        if spectral_centroid_mean < 1000 or spectral_centroid_mean > 3000:
            tone_score -= 10  # Low or high spectral centroid
        
        if rms_mean < 0.02:
            tone_score -= 15  # Low energy

        # Generate the audio feature summary for feedback
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

        # Create the prompt for LLM
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

        # Invoke the LLM for final feedback
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
