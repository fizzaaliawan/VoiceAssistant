# 🗣️ Voice Assistant (Python)

A smart **voice-controlled assistant** built in Python that can listen, talk, search Wikipedia, open apps/websites, do calculations, and interact casually.
This project uses **speech recognition** and **text-to-speech** technologies.

---

## 🚀 Features

* **Speech recognition** using `speech_recognition` + `sounddevice`.
* **Text-to-speech** with Google Text-to-Speech (`gTTS`).
* **Wikipedia integration** – Ask about anything and get a summary.
* **Open websites & apps** like YouTube, Google, Facebook, Notepad, Calculator.
* **Google search** directly with your voice.
* **Math calculations** (addition, subtraction, multiplication, division).
* **Time & Date** queries.
* **Casual conversation** (greetings, thanks, goodbye).
* Fun **jokes** & amazing **facts**.

---

## 🛠️ Requirements

Install the required libraries using pip:

```bash
pip install sounddevice numpy scipy SpeechRecognition gTTS playsound3 wikipedia
```

---


## 🎯 Example Commands

* **Time & Date** → "What time is it?", "Tell me today's date"
* **Wikipedia** → "Who is Albert Einstein?", "Tell me about Python"
* **Open apps/websites** → "Open YouTube", "Open calculator", "Open Notepad"
* **Google Search** → "Search artificial intelligence"
* **Math** → "12 plus 8", "45 divide 9"
* **Casual** → "Hello", "How are you?", "Thank you", "Goodbye"
* **Fun** → "Tell me a joke", "Tell me a fact"

---

## ⚡ How It Works

1. Records audio input using `sounddevice`.
2. Converts speech to text with **Google Speech Recognition**.
3. Matches the command against predefined categories.
4. Responds using **Google Text-to-Speech (gTTS)** + `playsound3`.
5. Executes actions like web search, Wikipedia summary, or app launching.


