# currency_classification.py

from edge_impulse_linux.image import ImageImpulseRunner
import cv2

MODEL_PATH = 'saisiddesh-project-1-linux-aarch64-v1.eim'

class CurrencyClassifier:
    def __init__(self):
        self.runner = ImageImpulseRunner(MODEL_PATH)
        self.model_info = self.runner.init()
        print("Currency model loaded. Labels:", self.model_info['model_parameters']['labels'])

    def classify(self, img):
        if img is None:
            print("Invalid image")
            return []

        _, results = self.runner.classify(img)
        return results['classification']

    def __del__(self):
        self.runner.stop()
