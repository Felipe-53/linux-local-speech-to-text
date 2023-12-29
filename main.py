import whisper
import subprocess
from logger import logger

MIC_SOURCE = "alsa_input.usb"


def transcribe_audio_from_file(file_path, english=True):
    model_name = "base.en"
    if not english:
        model_name = "base"

    model = whisper.load_model(model_name)
    result = model.transcribe(file_path)

    return result["text"]


if __name__ == "__main__":
    is_english = True

    result = subprocess.run(["pgrep", "pw-record"],
                            capture_output=True, encoding="utf-8")

    if result.stdout != "":
        subprocess.run(["pkill", "pw-record"], capture_output=True)

    else:
        source_id = None
        result = subprocess.run(
            ["pactl", "list", "short", "sources"], capture_output=True, encoding="utf-8")
        sources = result.stdout.split("\n")
        for source in sources:
            if MIC_SOURCE in source:
                source_id = source.split("\t")[0]

        record_command = ["pw-record", "audio.mp3"]
        logger.info("Microphone source not found, using default")
        if source_id != None:
            logger.info("Found microphone source: " + source_id)
            record_command = ["pw-record", "--target", source_id, "audio.mp3"]

        subprocess.run(["notify-send", "Speech-to-Text",
                        "Recording..."])

        subprocess.run(record_command, capture_output=True)

        subprocess.run(["notify-send", "Speech-to-Text",
                        "Transcribing your beautiful You voice..."])

        text = transcribe_audio_from_file("audio.mp3", is_english)

        subprocess.run(["wl-copy", text])

        # CTRL + V
        subprocess.run(["ydotool", "key", "97:1", "47:1", "97:0", "47:0"])
