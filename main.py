import whisper
import subprocess

def transcribe_audio_from_file(file_path, english = True):
    model_name = "base.en"
    if not english:
        model_name = "base"

    model = whisper.load_model(model_name)
    result = model.transcribe(file_path)

    return result["text"]
    


if __name__ == "__main__":
    is_english = True

    result = subprocess.run(["pgrep", "pw-record"], capture_output=True, encoding="utf-8")

    if result.stdout != "":
        subprocess.run(["pkill", "pw-record"], capture_output=True)
        
    else:
        subprocess.run(["pw-record", "audio.mp3"], capture_output=True)
        text = transcribe_audio_from_file("audio.mp3", is_english)
        subprocess.run(["wl-copy", text])
        subprocess.run(["ydotool", "type", "-d", "0", text])
        





