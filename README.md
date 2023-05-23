
# Zozo Assistant

Zozo Assistant is a Python-based voice-controlled assistant that uses natural language processing to answer questions and perform various tasks. The assistant can provide answers to pre-defined questions, play music, set alarms, tell the time and date, and engage in general conversation. It utilizes the OpenAI API for advanced language processing, but also includes a fallback pipeline model if the API is not available.

# Features
- Speech recognition: Zozo can listen to user input through a microphone and convert it into text using the SpeechRecognition library.
- Text-to-speech: Zozo can respond to users by converting text into speech using the pyttsx3 library.
- Music player: Zozo can play a collection of music files in the "music" folder. Users can control playback with voice commands or by entering options.
- Alarm: Users can set alarms by specifying the duration in seconds. Zozo will play a sound after the specified time has elapsed.
- Date and time: Users can inquire about the current date and time, and Zozo will provide the information.
- OpenAI integration: Utilize the OpenAI API for advanced language processing (API key required).
- Fallback pipeline model: If the OpenAI API is unavailable, the assistant falls back to a pre-trained pipeline model.


# Prerequisites

- Python 3.x
- pyaudio
- joblib
- nltk
- sklearn
- pygame 
- pyttsx3
- gTTS
- word2number
- SpeechRecognition
- jsonlib-python3
- openai 
- numpy
- pandas
# Getting Started
      

## Installation

1. Clone the repository:

```bash
  git clone https://github.com/Amirrezahmi/Zozo-Assistant.git

```
2. Install the required dependencies by running the following command:
```bash
  pip install -r requirements.txt
```
# Usage
3. Open the `main.py` file and locate the `OPENAI_API_KEY` variable. Paste your OpenAI API key into this variable.
4. If you don't have a microphone or encounter any issues with the microphone-related functions, you can replace all instances of `listen()` with `input()` in the code.
5. If `model2.joblib` dosen't work, delete it and run `train.py` again. Because sometimes the model only works on specefic version of Python that has trained before.
6. Run the `main.py` script to start the Zozo Assistant.
7. At the beggining say "Zozo" or "Hey Zozo" to get the Asisstant attention.
8. Interact with the chatbot by asking questions, playing music, setting alarms, or requesting the current date and time or any other prompts.
9. To exit the chatbot, say "bye", "goodbye" or "exit".

# Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2. Create a new branch: git checkout -b my-new-branch.
3. Make your changes and commit them: git commit -m 'Add some feature'.
4. Push to the branch: git push origin my-new-branch.
5. Submit a pull request.
    
## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).

# Credits

- [OpenAI](https://openai.com/)- For providing the chatbot API.
- [NLTK ](https://www.nltk.org/)- Natural Language Toolkit for text processing.
- [scikit-learn](https://scikit-learn.org/)- Machine learning library for building the question-answering model.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)- For audio input/output functionality.
- [pygame](https://www.pygame.org/)- Library for playing music files.
- [pyttsx3](https://pypi.org/project/pyttsx3/)- Text-to-speech library for speech output.
- [gTTS](https://gtts.readthedocs.io/en/latest/)- Google Text-to-Speech library for creating audio files from text.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)- Library for speech recognition functionality.
- [word2number](https://pypi.org/project/word2number/)- Library for converting words to numbers.


## Contact

For any questions or inquiries, please contact amirrezahmi2002@gmail.com

