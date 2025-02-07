from moviepy.editor import VideoFileClip, concatenate_videoclips

# Paths to the videos
original_video_path = "video1.mp4"
processed_video_path = "video22.mp4"
output_video_path = "final_output.mp4"

# Load the original and processed videos
original_clip = VideoFileClip(original_video_path).subclip(0,2.1)  # First 3 seconds
processed_clip = VideoFileClip(processed_video_path)  # Full processed video

# Extract the remaining part of the processed video (excluding first 3 sec)
processed_remaining = processed_clip.subclip(2.1, processed_clip.duration)

# Resize the original clip to match processed video's resolution & FPS
original_clip = original_clip.set_fps(processed_clip.fps).resize(processed_clip.size)

# Apply a smooth crossfade transition of 0.5 seconds
final_video = concatenate_videoclips([original_clip, processed_remaining], method="compose")

# Export the final video
final_video.write_videofile(output_video_path, codec="libx264", fps=processed_clip.fps, threads=4, preset="fast")



# # in middle middle 


# from moviepy.editor import VideoFileClip, concatenate_videoclips

# # Paths to the videos
# original_video_path = "video1.mp4"
# processed_video_path = "video22.mp4"
# output_video_path = "final_output.mp4"

# # Load the original and processed videos
# original_clip = VideoFileClip(original_video_path)
# processed_clip = VideoFileClip(processed_video_path)

# # Define the specific segments from the original video to insert
# original_segments = [
#     (0, 2),          # First segment: 0 to 2 seconds
#     (2.5, 3),        # Second segment: 2.5 to 3 seconds
#     (4.5, 5)         # Third segment: 4.5 to 5 seconds
# ]

# # Define the points in the processed video where the original segments will be inserted
# insert_points = [0, processed_clip.duration / 2, processed_clip.duration - 0.5]  # Start, middle, and near end

# # Ensure the insert points are within the bounds of the processed video
# insert_points = [max(0, min(point, processed_clip.duration)) for point in insert_points]

# # Extract segments from the processed video and insert original video segments
# final_clips = []
# start_time = 0

# for i, point in enumerate(sorted(insert_points)):
#     # Add the segment from the processed video before the insert point
#     if start_time < point:
#         final_clips.append(processed_clip.subclip(start_time, point))
    
#     # Add the corresponding segment from the original video
#     segment_start, segment_end = original_segments[i]
#     original_segment = original_clip.subclip(segment_start, segment_end).set_fps(processed_clip.fps).resize(processed_clip.size)
#     final_clips.append(original_segment)
    
#     # Update the start time
#     start_time = point

# # Add the remaining segment from the processed video
# if start_time < processed_clip.duration:
#     final_clips.append(processed_clip.subclip(start_time, processed_clip.duration))

# # Concatenate all the clips
# final_video = concatenate_videoclips(final_clips, method="compose")

# # Export the final video
# final_video.write_videofile(output_video_path, codec="libx264", fps=processed_clip.fps, threads=4, preset="fast")