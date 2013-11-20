import os
from tempfile import NamedTemporaryFile

from PIL import Image
from PyPDF2 import PdfFileReader
from wand.image import Image as WandImage
from tesserwrap import Tesseract


class PDFDocumentExtractor(object):
    def __init__(self, filename, config=None):
        filename = os.path.abspath(filename)
        print filename

        fileobj = open(filename, 'r+b')

        self.path = filename
        self.file = PdfFileReader(fileobj)
        self.config = {
            'wand_resolution': 300,
            'wand_compression_quality': 75
        }

        if config:
            self.config.update(config)

    def pages(self):
        for page in range(self.file.numPages):
            img = WandImage(filename=self.path + ('[%s]' % page),
                resolution=self.config['wand_resolution'])
            img.compression_quality = self.config['wand_compression_quality']
            temp = NamedTemporaryFile(suffix='.jpg')
            # Passing temp as file kwargs does not work for some reason.
            # So we just pass the filename.
            img.save(filename=temp.name)

            # Reopen the image file as PIL object
            img = Image.open(temp.name)

            # Run tesseract
            tr = Tesseract()
            result = tr.ocr_image(img)

            temp.close()

            yield result
