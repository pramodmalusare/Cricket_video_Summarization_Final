# from ultralytics import YOLO

# class YOLOModelWrapper:
#     def __init__(self, model_path):
#         self.model = YOLO(model_path)

#     def  run_detection(self, input_source, confidence_threshold=0.4, save_crop=True, save=True):
#         results = self.model.predict(source=input_source, conf=confidence_threshold, save_crop=save_crop, save=save)
#         return results

# def main():
#     model_path ="./ptfile/best.pt"
#     input_source = "./outputs/"

#     yolo_wrapper = YOLOModelWrapper(model_path)
#     detection_results = yolo_wrapper.run_detection(input_source)

# if __name__ == "__main__":
#     main()



#*******************************************************************************
from ultralytics import YOLO
import cv2
import os

class YOLOModelWrapper:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def run_detection(self, input_source, confidence_threshold=0.4, save_crop=True, save=True):
        results = self.model.predict(source=input_source, conf=confidence_threshold, save_crop=save_crop, save=save)
        return results

    def crop_and_save_scorecards(self, input_source, output_folder, detection_results):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for idx, result in enumerate(detection_results.xyxy[0]):
            class_id, confidence, xmin, ymin, xmax, ymax = map(int, result[:6])
            if class_id == 0:  # Assuming class_id 0 corresponds to the scorecard
                image_path = os.path.join(input_source, result[0])
                image = cv2.imread(image_path)
                cropped_scorecard = image[ymin:ymax, xmin:xmax]

                # Save each cropped scorecard separately in the output folder
                output_path = os.path.join(output_folder, f"scorecard_{confidence:.2f}_{idx}.png")
                cv2.imwrite(output_path, cropped_scorecard)

def main():
    model_path = "./ptfile/best.pt"
    input_source = "./outputs/"
    output_folder = "./cropped_scorecards/"

    yolo_wrapper = YOLOModelWrapper(model_path)
    detection_results = yolo_wrapper.run_detection(input_source)    
    yolo_wrapper.crop_and_save_scorecards(input_source, output_folder, detection_results)

if __name__ == "__main__":
    main()
