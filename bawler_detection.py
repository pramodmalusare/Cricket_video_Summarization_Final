import torch
from pathlib import Path
from PIL import Image
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

def yolov8_inference(weights_path, img_folder, output_folder, conf_thres=0.5, img_size=640):
    device = select_device('')
    model = attempt_load(weights_path, map_location=device)
    model.eval()

    img_folder = Path(img_folder)
    img_paths = sorted(img_folder.glob('*.jpg')) + sorted(img_folder.glob('*.png'))

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    for img_path in img_paths:
        img = torch.zeros((1, 3, img_size, img_size), device=device)  # initialize img
        img[0] = torch.from_numpy(img_path) / 255.0  # add image to batch

        pred = model(img)[0]  # predict
        pred = non_max_suppression(pred, conf_thres=conf_thres)[0]  # remove low-confidence detections

        if pred is not None and len(pred):
            pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], img_path.shape).round()

            img_with_boxes = Image.open(img_path).convert('RGB')
            for det in pred:
                plot_one_box(det, img_with_boxes, color=(0, 255, 0), label=f'Class {int(det[5])}, Conf {det[4]:.2f}')

            # Save the image with bounding boxes
            output_path = output_folder / img_path.name
            img_with_boxes.save(output_path)

if __name__ == "__main__":
    weights_path = '"C:\BE\Project Implemetations\Implementation\cricket_video_summarisation-master\weights-20240201T193059Z-001\weights\best.pt"'
    img_folder = 'C:\BE\Project Implemetations\Implementation\cricket_video_summarisation-master\outputs'
    output_folder = 'C:\BE\Project Implemetations\Implementation\cricket_video_summarisation-master\balwer_output'
    yolov8_inference(weights_path, img_folder, output_folder)
