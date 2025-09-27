# import cv2
# import os
# from pathlib import Path

# def pngs_to_video(input_folder, output_video, fps=30):
#     folder_path = Path(input_folder)
    
#     # Get all PNG files and sort them by modification time
#     png_files = sorted(
#         folder_path.glob("*.png"),
#         key=lambda x: x.stat().st_mtime
#     )

#     if not png_files:
#         print("No PNG files found in the folder.")
#         return

#     # Read first image to get dimensions
#     first_frame = cv2.imread(str(png_files[0]))
#     if first_frame is None:
#         print(f"Could not read image: {png_files[0]}")
#         return

#     height, width, _ = first_frame.shape

#     # Initialize video writer
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

#     for img_path in png_files:
#         frame = cv2.imread(str(img_path))
#         if frame is None:
#             print(f"Skipping unreadable image: {img_path.name}")
#             continue
#         if frame.shape[:2] != (height, width):
#             frame = cv2.resize(frame, (width, height))
#         out.write(frame)

#     out.release()
#     print(f"✅ Video created at: {output_video}")

# # Example usage
# if __name__ == "__main__":
#     input_folder = "D:/Weekly Meetings/Synopsis PPT/Video/Cascades 7/"     # Replace with actual folder path
    
#     fps_manual = 5
#     output_video = f"output_video_{fps_manual}.mp4"        # Output filename
#     # pngs_to_video(input_folder, output_video, fps=fps_manual)
#     pngs_to_video(input_folder, output_video, fps=fps_manual)













import cv2
import os
from pathlib import Path
from pdf2image import convert_from_path

def pdfs_to_video(input_folder, output_video, fps=30, seconds_per_page=2, poppler_path=None):
    folder_path = Path(input_folder)
    pdf_files = sorted(folder_path.glob("*.pdf"), key=lambda x: x.stat().st_mtime)

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    frames = []

    for pdf_path in pdf_files:
        try:
            # Convert only the first page of each PDF to an image
            pages = convert_from_path(str(pdf_path), dpi=200, poppler_path=poppler_path)
            if pages:
                img = pages[0]
                frames.append(img)
        except Exception as e:
            print(f"⚠️ Error processing {pdf_path.name}: {e}")

    if not frames:
        print("No pages converted from PDFs.")
        return

    # Get dimensions from the first image
    first_frame = frames[0]
    width, height = first_frame.size
    video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    repeat_count = int(fps * seconds_per_page)

    for img in frames:
        # Convert PIL Image to OpenCV format
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Resize if needed
        if (frame.shape[1], frame.shape[0]) != (width, height):
            frame = cv2.resize(frame, (width, height))

        for _ in range(repeat_count):
            video_writer.write(frame)

    video_writer.release()
    print(f"✅ Video saved to: {output_video}")

# Example usage
if __name__ == "__main__":
    import numpy as np
    

    # instance_name = "4C Level2 Cascades6"
    # instance_name = "6A Level2 Cascade7"
    # instance_name = "6B Level2 Cascade7"
    instance_name = "4C Level2 Cascades6"

    

    input_folder = f"D:/Weekly Meetings/Synopsis PPT/Video/{instance_name}/"        # Change to your folder path
    
    
    seconds_per_image = 2
    output_video = f"{instance_name}_{seconds_per_image}.mp4"
    pdfs_to_video(input_folder, output_video, fps=24, seconds_per_page=seconds_per_image)
