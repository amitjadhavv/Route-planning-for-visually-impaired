import argparse
from sensation.data_handler import InputHandler
from sensation.helper.segmentation import Segmentator
import cv2

def calculate_valhalla():
    pass

def estimate_velocity():
    pass

def get_current_street_name():
    pass

def main():
    parser = argparse.ArgumentParser(description="RSU_VI input handler")
    parser.add_argument('input_path',help="path to input video")
    parser.add_argument('gps_path',help="path to gps coordinates")
    parser.add_argument('output_path',help="path to output video")

    args = parser.parse_args()

    ih = InputHandler(input_path=args.input_path,output_path=args.output_path)
    segmentator = Segmentator(model_path=args.model_path, input_height=256, input_width=512)

    route, instruction = calculate_valhalla()

    velocity = estimate_velocity()

    current_street = get_current_street_name()

    frame_width = int(ih.get_cap().get(3))
    frame_height = int(ih.get_cap().get(4))
    output = cv2.VideoWriter(args.output_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))
    
