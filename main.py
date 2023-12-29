import whisper
import subprocess
from logger import logger
import sys

MIC_SOURCE = "alsa_input.usb"


def transcribe_audio_from_file(file_path, english=True):
    model_name = "base.en"
    language = "en"

    if not english:
        model_name = "base"
        language = "pt"

    model = whisper.load_model(model_name)
    result = model.transcribe(file_path, language=language)

    return result["text"]


if __name__ == "__main__":
    is_english = True

    logger.info("Starting Speech-to-Text")

    try:

        if len(sys.argv) > 1:
            if sys.argv[1] == "pt":
                logger.info("Transcribing in portuguese")
                is_english = False
        else:
            logger.info("Transcribing in english")

        result = subprocess.run(["pgrep", "pw-record"],
                                capture_output=True, encoding="utf-8", check=True)

        if result.stdout != "":
            subprocess.run(["pkill", "pw-record"],
                           capture_output=True, check=True)

        else:
            source_id = None
            result = subprocess.run(
                ["pactl", "list", "short", "sources"], capture_output=True, encoding="utf-8", check=True)
            sources = result.stdout.split("\n")
            for source in sources:
                if MIC_SOURCE in source:
                    source_id = source.split("\t")[0]

            if source_id is not None:
                logger.info("Found microphone source: %s", source_id)
                record_command = ["pw-record",
                                  "--target", source_id, "audio.mp3"]
            else:
                record_command = ["pw-record", "audio.mp3"]
                logger.info("Microphone source not found, using default")

            subprocess.run(["notify-send", "Speech-to-Text",
                            "Recording..."], check=True)

            subprocess.run(record_command, capture_output=True, check=True)

            subprocess.run(["notify-send", "Speech-to-Text",
                            "Transcribing your beautiful voice..."], check=True)

            text = transcribe_audio_from_file("audio.mp3", is_english)

            subprocess.run(["wl-copy", text], check=True)

            # CTRL + V
            subprocess.run(["ydotool", "key", "97:1", "47:1",
                           "97:0", "47:0"], check=True)

    # pylint: disable=broad-except
    except Exception as e:
        logger.error(e)
        subprocess.run(["notify-send", "--urgency", "critical", "--expire-time", "1000", "Speech-to-Text",
                        "An error occurred, check the logs"], check=True)
