
# Zozo Assistant

Zozo Assistant is a Python-based voice-controlled assistant that uses natural language processing to answer questions and perform various tasks. But also you can use it if you don't have a microphone. The assistant can provide answers to pre-defined questions, play music, say weather, set alarms, tell the time and date, and engage in general conversation. This application leverages the OpenAI API for sophisticated language processing, but also includes a fallback pipeline model for situations where the API is not accessible. The code in `train.py` trains a chatbot using a Linear Support Vector Machine (SVM) classifier. It reads a dataset from a file named `datamain.txt`, which contains a collection of questions and corresponding answers. The chatbot learns from this dataset and creates a pipeline model using the `CountVectorizer`, `TfidfTransformer`, and `LinearSVC` from scikit-learn. The text data is preprocessed using a custom function that removes punctuation, converts text to lowercase, and applies lemmatization to reduce words to their base or root form. This preprocessing step helps to improve the model's ability to understand and respond to a variety of inputs. Once trained, the model is saved as `model2.joblib` for future use when the API is not available.

## Features
- Speech recognition: Zozo can listen to user input through a microphone and convert it into text using the SpeechRecognition library.
- Text-to-speech: Zozo can respond to users by converting text into speech using the pyttsx3 library.
- Weather: Users can ask for the current weather information for a location, and Zozo will provide the information.
- Music player: Zozo can play a collection of music files in the "music" folder. Users can control playback with voice commands or by entering options.
- Alarm: Users can set alarms by specifying the duration in seconds. Zozo will play a sound after the specified time has elapsed.
- Date and time: Users can inquire about the current date and time, and Zozo will provide the information.
- OpenAI integration: Utilize the OpenAI API for advanced language processing (API key required).
- Fallback pipeline model: If the OpenAI API is unavailable, the assistant falls back to a pre-trained pipeline model.
- Clean and minimalist UI design

# Prerequisites

- Python 3.x
- [OpenAI API](https://openai.com/)
- [OpenWeather API](https://openweathermap.org/)
- pyaudio
- joblib
- nltk
- scikit-learn
- pygame
- tkinter
- requests 
- pyttsx3
- word2number
- SpeechRecognition
- jsonlib-python3
- openai 
- numpy
- pandas
# Getting Started
      

# Installation

1. Clone the repository:

```bash
  git clone https://github.com/Amirrezahmi/Zozo-Assistant.git

```

2. Navigate to the project directory:

```bash

  cd Zozo-Assistant

```
3. Install the required dependencies by running the following command:
```bash
  pip install -r requirements.txt
```
4. As stated earlier, we are using `pyttsx3` in this program. It is essential to note that this program has been developed on a Windows-powered device, which may result in encountering errors with certain libraries on other operating systems, such as pyttsx3. pyttsx3 uses speech synthesis engines that depend on your operating system. Make sure that the corresponding speech engine is correctly installed and configured. For example, on Linux, pyttsx3 uses espeak. You might need to install it in case you are using Linux:
```bash
sudo apt-get update && sudo apt-get install espeak
```
## Usage
5. Open the `main.py` and `ui.py` files and locate the `OPENAI_API_KEY` and `apiKey` variables. Paste your OpenAI API key into `OPENAI_API_KEY` variable, and paste your OpenWeather API key into `apiKey` variable.
6. If you don't have a microphone or encounter any issues with the microphone-related functions, in the beginning of running `main.py` the program asks you that do you have a microphone or not and you can answer no if you don't. In `ui.py` I haven't implemented a microphone button yet and you should write your input prompt or use buttons, but I'll implement a button for microphone soon!
7. If `model2.joblib` dosen't work, delete it and run `train.py` again. Because sometimes the model only works on specefic version of Python that has trained before.
8. Run the `main.py` script (for console-based) or `ui.py` script (for user interface (UI)) to start the Zozo Assistant.
9. At the beggining say "Zozo" or "Hey Zozo" to get the Asisstant attention. (If you chossed the microphone option at the begging.)
10. Interact with the chatbot by asking questions, playing music, weather, setting alarms, or requesting the current date and time or any other prompts.
11. To exit the chatbot, say "bye", "goodbye" or "exit".


# Basic and Intuitive User Interface

Zozo Assistant has undergone a transformation from a console-based project to a visually captivating user interface (UI). Although the UI remains basic, it provides a simple and intuitive way for users to interact with the assistant, enhancing their overall experience.

## Key Features:

- Basic and minimalist UI design that focuses on functionality.
- Easy navigation through the assistant's features.
- Intuitive controls and straightforward interaction methods.
- Streamlined functionality for seamless execution of commands.

Despite its basic nature, the UI of Zozo Assistant ensures that users can effortlessly interact with the assistant's capabilities without any unnecessary complexity. The clean and minimalist design allows for a distraction-free experience, enabling users to focus on the assistant's functionality and make the most out of their interactions.

Feel free to modify the text according to your preferences and specific features of your UI.

# Examples

This section includes hands-on, practical examples demonstrating how to interact with the Zozo-Assistant. Here, you will find examples for both console-based and GUI-based interactions.

## Console-based Interactions

Uncover different scenarios for interacting with the Zozo-Assistant using the console. This section delves into specific situations, portraying what happens when the microphone is accessible and when it isn't.

### Scenario: Microphone Inaccessible

This part describes the interaction flow when the user does not grant microphone access. After the initial question from the program about microphone accessibility, if the user responds with "no", the subsequent interaction process unfolds as demonstrated in the screenshot below:

<div align="center">
  <img src="https://github.com/Amirrezahmi/Zozo-Assistant/assets/89692207/3c3f191c-7e97-4a72-b096-02388e8ea685" width="800" />
</div>


### Scenario: Microphone Accessible

A video demonstration showcasing what happens when the user provides microphone access — that is, when the microphone accessibility question is answered with a "yes". This video depicts how the program responds and guides on the subsequent steps the user needs to take.





https://github.com/Amirrezahmi/Zozo-Assistant/assets/89692207/5902b33c-ff2b-42a2-babe-e8729c89fc21





## GUI Interactions

This section contains a visual guide on how to navigate and interact with the Zozo-Assistant using the graphical user interface (GUI).






https://github.com/Amirrezahmi/Zozo-Assistant/assets/89692207/4f21aac2-1aa5-47c4-926c-509743b6e8a2







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
- [tkinter](https://docs.python.org/3/library/tkinter.html)- For creating the user interface (UI) components.
- [NLTK ](https://www.nltk.org/)- Natural Language Toolkit for text processing.
- [scikit-learn](https://scikit-learn.org/)- Machine learning library for building the question-answering model.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)- For audio input/output functionality.
- [pygame](https://www.pygame.org/)- Library for playing music files.
- [pyttsx3](https://pypi.org/project/pyttsx3/)- Text-to-speech library for speech output.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)- Library for speech recognition functionality.
- [word2number](https://pypi.org/project/word2number/)- Library for converting words to numbers.


## Contact

For any questions or inquiries, please contact amirrezahmi2002@gmail.com

