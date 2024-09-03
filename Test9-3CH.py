import pyperclip
import speech_recognition as sr
import webbrowser
import time
import os
import pyautogui
import random
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from io import BytesIO
import re
import sympy as sp


def Talk(audio):
    """Function that speaks using Google Text-to-Speech"""
    try:
        tts = gTTS(text=audio, lang='ar')
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        
        audio_segment = AudioSegment.from_file(audio_data, format="mp3")
        play(audio_segment)
    except Exception as e:
        print(f"Error in Talk: {e}")


def TakeOrder():
    """Function to take a voice command from the user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print('Listening for "Hey Bella"...')
        recognizer.phrase_threshold = 0.4
        while True:
            try:
                audio = recognizer.listen(mic, timeout=5)  # Timeout to reset the listen loop
                order = recognizer.recognize_google(audio, language='ar')
                print(f'You Said  ==>  "{order}"')
                if "هي بيلا" in order or "hey bella" in order.lower():
                    Talk('نعم؟ كيف يمكنني مساعدتك؟')  # Respond to wake word
                    return ListenForCommand()  # Listen for the actual command after wake word
            except sr.UnknownValueError:
                continue  # Continue listening if the wake word isn't detected
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                Talk('لَمْ أَتَمَكَّنْ مِنْ تَنْفِيذِ النَّتِيجَة.')
            except Exception as Error:
                print(f"An error occurred: {Error}")
                Talk('لَقَدْ حَدَّثَ خَطَأ.')


def ListenForCommand():
    """Function to take a voice command after hearing the wake word"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print('Say your command...')
        recognizer.phrase_threshold = 0.4
        audio = recognizer.listen(mic)
        try:
            print('Recording...')
            order = recognizer.recognize_google(audio, language='ar')
            print(f'You Said  ==>  "{order}"')
            return order.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
            Talk('لَمْ أَفْهَمْ مَاذَا تُقْصَد. هَلْ يُمْكِنُك أَنْ تَقُولَ مَرَّةً أُخْرَى.')
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            Talk('لَمْ أَتَمَكَّنْ مِنْ تَنْفِيذِ النَّتِيجَة.')
        except Exception as Error:
            print(f"An error occurred: {Error}")
            Talk('لَقَدْ حَدَّثَ خَطَأ.')

    return None


def play_sound(file_path):
    """Function to play an MP3 sound file"""
    try:
        audio = AudioSegment.from_mp3(file_path)
        play(audio)
    except FileNotFoundError:
        print(f"Sound file not found: {file_path}")
        Talk('لَمْ يَتِمَّ الْعُثُورِ عَلَى مَلْف الصَّوْتِ.')
    except Exception as e:
        print(f"An error occurred while playing the sound: {e}")
        Talk('لَقَدْ حَدَّثَ خَطَأً عِنْدَ تَشْغِيل الصَّوْت.')


def Answer(Main_Words, path, order):
    """Function to respond based on specific keywords in the order"""
    two_words_together = [' '.join(order[i:i+2]) for i in range(len(order)-1)]

    # Strip "و" prefix if present
    two_words_together = [element.lstrip('و') if element.startswith('و') else element for element in two_words_together]

    joint = list(Main_Words.intersection(two_words_together))

    if joint:
        play_sound(path)


def calculate_expression(expression):
    """Evaluates a mathematical expression safely using sympy"""
    try:
        # Clean and translate Arabic digits if needed
        expression = re.sub(r'[٠١٢٣٤٥٦٧٨٩]', lambda x: str(ord(x.group()) - 1632), expression)
        result = sp.sympify(expression)
        print(f"Calculation result: {result}")
        Talk(f'الناتج هو {result}')
    except Exception as e:
        print(f"An error occurred while calculating: {e}")
        Talk('لَقَدْ حَدَّثَ خَطَأً فِي الْحِسَاب.')


# Initialize and start interaction
play_sound("sounds/EsmakEh.mp3")

name = TakeOrder()

play_sound("sounds/Asa3dakEzay.mp3")

# Define word groups for specific responses
Main_Words_1 = {
    "تخصصات مصر", "اقسام مصر", "تخصصات الكليه", "تخصصات الجامعه", "تخصصات جامعه", 
    "تخصصات كليه", "ايه اقسامها", "اقسامها ايه", "اقسام الكليه", "اقسام الجامعه", 
    "اقسام جامعه", "اقسام كليه", "تخصصاتها ايه"
}
Main_Words_2 = {"مكان", "مكانها", "موقع", "موقعها", 'المكان', 'الموقع'}
Main_Words_3 = {"فطار", "اكل", "فول", "طعميه"}
Main_Words_4 = {"نامي", "اتخمدي"}
Main_Words_5 = {"تاريخ"}

while True:
    order = TakeOrder()  # First listen for "Hey Bella"
    if order is None:
        continue
    order = order.split()

    if "احسب" in order:  # Look for calculation command
        calculation = ' '.join(order[order.index("احسب") + 1:])  # Get the expression to calculate
        calculate_expression(calculation)
        continue

    Answer(Main_Words_1, random.choice(['sounds/Takhsosat.mp3', 'sounds/Asa3dakEzay.mp3', 'sounds/7ader3yony.mp3']), order)
    Answer(Main_Words_4, "sounds/Tsba73ala5eir.mp3", order)

    if "نامي" in order or "اتخمدي" in order:
        play_sound("sounds/Tsba73ala5eir.mp3")
        break

    elif "عاوز اسمع اغاني" in order:
        play_sound('sounds/Ash8alkEh.mp3')
        post = ListenForCommand()
        play_sound('sounds/7ader3yony.mp3')

        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(r'C:\Program Files\Google\Chrome\Application\chrome.exe'))
        pyautogui.hotkey('ctrl', 't')
        link = r'https://www.youtube.com'
        webbrowser.get('chrome').open_new_tab(link)

        time.sleep(4)
        pyautogui.click(726, 144)  # Adjust these coordinates based on your screen resolution

        pyperclip.copy(post)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        time.sleep(3)
        pyautogui.click(1006, 535)  # Adjust these coordinates based on your screen resolution
