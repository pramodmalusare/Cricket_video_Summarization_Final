from frame_extractor import FrameExtractor
from text_extractor import TextExtractionUsingOCR
from yolo import YOLOModelWrapper

if __name__ == "__main__":
    video_path = "./inputs/cricket_video.mp4"
    extracted_frame_dir = "./outputs/"
    # Frame Extraction
    # frame_extractor = FrameExtractor(video_path, extracted_frame_dir)
    # frame_extractor.extract_frames_by_framecount(1000)#enter appropriate frame count
    # frame_extractor.extract_frames_by_percentage(60)
    print("Frames extracted successfully.")

    # #finding Scoreboard using yolo
    model_path = "./ptfile/best.pt"
    model_input_source_path = extracted_frame_dir
    
    yolo_wrapper = YOLOModelWrapper(model_path)
    detection_results = yolo_wrapper.run_detection(model_input_source_path)
    print(detection_results)

    # #getting text module
    # # input_text_extractor=r"D:\BE Final Year Project\workspace\runs\detect\predict\crops\scorecard"
    # input_text_extractor="D:\BE Final Year Project\workspace\output\extracted_frames"
    # text_file_name=input("Enter text file name ")
    # text_extractor = TextExtractionUsingOCR(input_text_extractor, text_file_name)
    # text_extractor.process_frames()



