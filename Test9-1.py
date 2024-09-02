import pyperclip, speech_recognition as sr, webbrowser, time, datetime, os,pyautogui, random
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS


def Talk(audio):

    """Function Bttklm Be Sot Google"""
    
    tts = gTTS(text=audio, lang='ar')
    tts.save('temp.mp3')
    
    audio_segment = AudioSegment.from_mp3('temp.mp3')
    play(audio_segment)
    
    os.remove('temp.mp3')



def TakeOrder():

    """ Function Bta5od El Order (El So2al) """

    command = sr.Recognizer()
    with sr.Microphone() as Mic:
        print('Say Order...')
        command.phrase_threshold = 0.4
        audio = command.listen(Mic)
        try:
            print('Recording...')
            order = command.recognize_google(audio, language='ar')
            print(f'You Said  ==>  " {order} " ')
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
            Talk('لَمْ أَفْهَمْ مَاذَا تُقْصَد. هَلْ يُمْكِنُك أَنْ تَقُولَ مَرَّةً أُخْرَى.')
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            Talk('لَمْ أَتَمَكَّنْ مِنْ تَنْفِيذِ النَّتِيجَة .')
            return None
        except Exception as Error:
            print(f"An error occurred: {Error}")
            Talk('لَقَدْ حَدَّثَ خَطَأ .')
            
            return None

        return order.lower()

def play_sound(file_path):

    """ Function Btsh3'l El Mp3 """

    try:
        audio = AudioSegment.from_mp3(file_path)
        play(audio)

    except FileNotFoundError:
        print(f"Sound file not found: {file_path}")
        Talk('لَمْ يَتِمَّ الْعُثُورِ عَلَى مَلْف الصَّوْتِ .')

    except Exception as e:
        print(f"An error occurred while playing the sound: {e}")
        Talk('لَقَدْ حَدَّثَ خَطَأً عِنْدَ تَشْغِيل الصَّوْت .')





def Answer(Main_Words,path):
    
    """ Function 3ashan N7ot Feha Questions Malhash 3elaka Be El Gam3a """

    Two_Words_Together = []

    for i in range(0,len(order)-1):


        Two_Words_Together.append(order[i] + ' ' + order[i+1])
        for element in Two_Words_Together:
            if element.startswith('و'):
                element = element.lstrip('و')
    element = [element]
    joint=list(Main_Words.intersection(element))

    try:
        word=joint[0]
        main1={word}
        if main1.issubset(Main_Words):

            play_sound(path)

    except:
        pass



play_sound("sounds/EsmakEh.mp3")


name = TakeOrder()


play_sound("sounds/Asa3dakEzay.mp3")





Main_Words_1={"تخصصات مصر","اقسام مصر","تخصصات الكليه","تخصصات الجامعه","تخصصات جامعه","تخصصات كليه","ايه اقسامها"\
              "اقسامها ايه","اقسام الكليه","اقسام الجامعه","اقسام جامعه","اقسام كليه","اقسامها ايه","تخصصاتها ايه"}
Main_Words_2={"مكان","مكانها","موقع","موقعها",'المكان','الموقع'}
Main_Words_3={"فطار","اكل","فول","طعميه"}
Main_Words_4={"نامي","اتخمدي"}
Main_Words_5={"تاريخ"}



while True:
    order = TakeOrder()
    if order is None:
        continue
    order=order.split()


    Answer(Main_Words_1,"".join(random.choices(['sounds/Takhsosat.mp3','sounds/Asa3dakEzay.mp3','sounds/7ader3yony.mp3'])))
    # Answer(Main_Words_2,'sounds/Asa3dakEzay.mp3')
    # Answer(Main_Words_3,'sounds/7ader3yony.mp3')
    Answer(Main_Words_4,"sounds/Tsba73ala5eir.mp3")


    if "نامي" in order or "اتخمدي" in order:
        play_sound("sounds/Tsba73ala5eir.mp3")
        break




    elif "عاوز اسمع اغاني" in order:

        play_sound('sounds/Ash8alkEh.mp3')

        # Talk("تحب أشغلك ايه؟")           ############

        post = TakeOrder()

        # Talk("حاضر أنا عيوني ليك")        ############

        play_sound('sounds/7ader3yony.mp3')

        webbrowser.register('chrome', None,
                            webbrowser.BackgroundBrowser(r'C:\Program Files\Google\Chrome\Application\chrome.exe'))
        pyautogui.hotkey('ctrl', 't')
        link = r'https://www.youtube.com'
        webbrowser.get('chrome').open_new_tab(link)

        time.sleep(4)

        pyautogui.click(726, 144)

        pyperclip.copy(post)
        pyautogui.hotkey('ctrl' , 'v')
        pyautogui.press('enter')


        time.sleep(3)
        pyautogui.click(1006, 535)