import whisper

def extract_transcript(audio_path: str) -> str:
    try:
        print(f"🔍 [Whisper] Extracting transcript from: {audio_path}")
        

        print("📥 [Whisper] Import successful")

        model = whisper.load_model("base")
        print("✅ [Whisper] Model loaded")

        result = model.transcribe(audio_path)
        print("📝 [Whisper] Transcript (first 100 chars):", result.get("text", "")[:100])

        return result["text"]
        
    except Exception as e:
        print(f"❌ Whisper Error: {e}")
        return "Transcript extraction failed."
