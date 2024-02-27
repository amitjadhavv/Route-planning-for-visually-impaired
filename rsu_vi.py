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

def find_dominant_column():
    pass

def main():
    parser = argparse.ArgumentParser(description="RSU_VI input handler")
    parser.add_argument('input_path',help="path to input video")
    parser.add_argument('gps_path',help="path to gps coordinates")
    parser.add_argument('output_path',help="path to output video")

    args = parser.parse_args()

    ih = InputHandler(input_path=args.input_path,output_path=args.output_path)
    segmentator = Segmentator(model_path=args.model_path, input_height=256, input_width=512)

    route, instructions = calculate_valhalla()

    velocity = estimate_velocity()

    current_street = get_current_street_name()

    frame_width = int(ih.get_cap().get(3))
    frame_height = int(ih.get_cap().get(4))
    output = cv2.VideoWriter(args.output_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

    count_frame = 0
    while True:
        ret, frame = ih.get_cap().read()
        if not ret:
            break

        if count_frame % 60 == 0:  # Check every 2 seconds (assuming 30 fps)
            dominant_column_command = find_dominant_column(frame, segmentator)

        # Placeholder for displaying navigation information
        navigation_info = f"Instruction from Valhalla: {instructions}\n" \
                           f"Command from Valhalla: {route}\n" \
                           f"Estimated Speed: {velocity}\n" \
                           f"Current street name: {current_street}\n" \
                           f"Command from segmentation: {dominant_column_command}\n" \
                           f"Total time: {total_time}, Elapsed time: {elapsed_time}"

        # Add white box with navigation information
        cv2.rectangle(frame, (0, 0), (300, 150), (255, 255, 255), -1)
        cv2.putText(frame, "Navigation Information", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.putText(frame, navigation_info, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        output.write(frame)
        count_frame += 1

        cv2.imshow('Navigation Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ih.get_cap().release()
    output.release()
    cv2.destroyAllWindows()
