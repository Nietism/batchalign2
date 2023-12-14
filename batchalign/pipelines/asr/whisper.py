from batchalign.document import *
from batchalign.pipelines.base import *
from batchalign.pipelines.asr.utils import *
from batchalign.models.asr import WhisperModel, WhisperProcessor, WhisperTokenizer

import pycountry

class WhisperEngine(BatchalignEngine):
    tasks = [ Task.ASR, Task.UTTERANCE_SEGMENTATION ]

    def __init__(self, model=None, lang_code="eng"):

        if model == None and lang_code == "eng":
            model = "talkbank/CHATWhisper-en-large-v1"
        elif model == None:
            model = "openai/whisper-large-v2"

        language = pycountry.languages.get(alpha_3=lang_code).name
            
        self.__whisper = WhisperModel(model, language=language)
        self.__lang = lang_code

    def generate(self, source_path):
        res = self.__whisper(self.__whisper.load(source_path).all())
        doc = process_generation(res, self.__lang)

        # define media tier
        media = Media(type=MediaType.AUDIO, name=Path(source_path).stem, url=source_path)
        doc.media = media

        return doc


    # model="openai/whisper-large-v2", language="english"

# e = WhisperEngine()
# tmp = e.generate("./batchalign/tests/pipelines/asr/support/test.mp3", 1)
# tmp.model_dump()
# file = "./batchalign/tests/pipelines/asr/support/test.mp3"


