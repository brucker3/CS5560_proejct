from gtts import gTTS
import os
from pygame import mixer


class TextToSpeech:
    def __init__(self):
        self.language = 'en'
        self.save_path = './audio/tmp.mp3'
        if not os.path.isdir('./audio'):
            os.mkdir('./audio')
        self.flag = True

    def load(self, text):
        assert isinstance(text, str)
        result = gTTS(text=text, lang=self.language, slow=False)
        result.save(self.save_path)
        os.system(f"ffmpeg -y -i ./audio/tmp.mp3 ./audio/tmp.ogg")
        # os.system("mpg321 ./tmp.mp3")
        # os.remove("./tmp.mp3")
        mixer.init()
        mixer.music.load('./audio/tmp.ogg')

    def play(self):
        mixer.music.play()

    def pause_unpause(self):
        if self.flag:
            mixer.music.pause()
            self.flag = False
        else:
            mixer.music.unpause()
            self.flag = True

    def stop(self):
        mixer.music.stop()
#
# model = TextToSpeech()
# model('Welcome hi hi qwerfdsadcv dsadjkfnnkms asdjfvhbjsakdfmv')
# model.play()
# model.pause_unpause()
# model.pause_unpause()
# model.stop()
