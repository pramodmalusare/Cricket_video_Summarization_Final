# import os
# import cv2
# import pytesseract
# import re
# from tqdm import tqdm


# class TextExtractionUsingOCR:
#     def __init__(self, folder_path, output_file_name):
#         self.folder_path = folder_path
#         self.output_file_path = (
#             "C:\BE\Project Implemetations\Rohit Code\cricket_video_summarisation-master\output_ocr_text/" + output_file_name
#         )
#         print(self.output_file_path)

#         pytesseract.pytesseract.tesseract_cmd = (
#             r"C:/Program Files/Tesseract-OCR/tesseract.exe"
#         )
#         print(f"Applying OCR on files in  {self.folder_path}")

#     def extract_text(self, image_path):
#         text = pytesseract.image_to_string(image_path, config="--psm 13")
#         return text

#     def process_frames(self):
#         # Open the text file in write mode
#         with open(self.output_file_path, "w") as output_file:
#             # Get the total number of frames for the progress bar
#             total_frames = len(
#                 [
#                     f
#                     for f in os.listdir(self.folder_path)
#                     if f.endswith((".png", ".jpg", ".jpeg"))
#                 ]
#             )
#             # Initialize the tqdm progress bar
#             for frame_name in tqdm(
#                 os.listdir(self.folder_path),
#                 total=total_frames,
#                 desc="Processing Frames",
#             ):
#                 # for frame_name in os.listdir(self.folder_path):
#                 if frame_name.endswith((".png", ".jpg", ".jpeg")):
#                     frame_path = os.path.join(self.folder_path, frame_name)
#                     # Extract text from the current frame
#                     scorecard_text = self.extract_text(frame_path)
#                     pattern = r'frameNo(?P<image_name>frame_\d+\.jpg)=>.*?(\b\s*(?P<fours>\d+)\s*Four\b)?.*?(\b\s*(?P<sixes>\d+)\s*Six\b)?.*?(\b\s*(?P<wickets>\d+)\s*Wicket\b)?.*'
#                     match = re.findall(pattern, scorecard_text)
#                     output_file.write(
#                         f"frameNo{frame_name}=>{scorecard_text}-------{match}\n\n"
#                     )
#         print(f"Extracted text has been saved to {self.output_file_path}")


# def main():
#     frames_folder = (
#         r"C:/Users/omkar/runs\detect/predict7/crops/scorecard"
#     )
#     # output_file_path="D:\BE Final Year Project\workspace\ocrouput\c.txt"
#     textextractor = TextExtractionUsingOCR(frames_folder, "3.txt")
#     textextractor.process_frames()


# if __name__ == "__main__":
#     main()

#*********************************************************
import os
import cv2
import pytesseract
import re
import csv
from tqdm import tqdm

class TextExtractionUsingOCR:
    def __init__(self, folder_path, output_file_name):
        self.folder_path = folder_path
        self.output_file_path = os.path.join(
            "C:/BE/Project Implemetations/Rohit Code/cricket_video_summarisation-master/output_ocr_text/",
            output_file_name
        )
        print(self.output_file_path)

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:/Program Files/Tesseract-OCR/tesseract.exe"
        )
        print(f"Applying OCR on files in  {self.folder_path}")

    def extract_text(self, image_path):
        text = pytesseract.image_to_string(image_path, config="--psm 13")
        return text

    def process_frames(self):
        # Open the CSV file in write mode
        with open(self.output_file_path, "w", newline='', encoding='utf-8') as output_file:
            # Create a CSV writer
            csv_writer = csv.writer(output_file)
            # Write header to the CSV file
            csv_writer.writerow(['Frame Name', 'Fours', 'Sixes', 'Wickets'])
            
            # Get the total number of frames for the progress bar
            frames_list = [
                f
                for f in os.listdir(self.folder_path)
                if f.endswith((".png", ".jpg", ".jpeg"))
            ]
            total_frames = len(frames_list)
            
            # Initialize the tqdm progress bar
            for frame_name in tqdm(
                frames_list,
                total=total_frames,
                desc="Processing Frames",
                unit="frames",
            ):
                frame_path = os.path.join(self.folder_path, frame_name)
                # Extract text from the current frame
                scorecard_text = self.extract_text(frame_path)
                
                # Count the occurrences of 'Four', 'Six', and 'Wicket'
                fours_count = scorecard_text.lower().count('four')
                sixes_count = scorecard_text.lower().count('six')
                wickets_count = scorecard_text.lower().count('wicket')
                
                # Write information to the CSV file
                csv_writer.writerow([frame_name, fours_count, sixes_count, wickets_count])

        print(f"Extracted information has been saved to {self.output_file_path}")

def main():
    frames_folder = r"C:/Users/omkar/runs\detect/predict7/crops/scorecard"
    textextractor = TextExtractionUsingOCR(frames_folder, "output_info.csv")
    textextractor.process_frames()

if __name__ == "__main__":
    main()
