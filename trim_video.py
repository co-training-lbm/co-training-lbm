#!/usr/bin/env python3
"""
Script to trim a .mov video file and convert it to web-compatible .mp4 format.

Usage:
    python3 trim_video.py input.mov start_time end_time [output.mp4]

Examples:
    python3 trim_video.py video.mov 00:00:10 00:01:30
    python3 trim_video.py video.mov 00:00:10 00:01:30 output.mp4
    python3 trim_video.py video.mov 10 90  # Using seconds
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def parse_time(time_str):
    """
    Parse time string in format HH:MM:SS or just seconds.
    Returns time in seconds.
    """
    if ':' in time_str:
        # Format: HH:MM:SS or MM:SS
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    else:
        # Just seconds
        return float(time_str)


def format_time(seconds):
    """Format seconds as HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{int(minutes):02d}:{secs:06.3f}"


def trim_video(input_file, start_time, end_time, output_file=None):
    """
    Trim a video file from start_time to end_time and convert to web-compatible MP4.
    
    Args:
        input_file: Path to input .mov file
        start_time: Start time (can be HH:MM:SS or seconds)
        end_time: End time (can be HH:MM:SS or seconds)
        output_file: Optional output file path. If not provided, generates from input filename.
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Parse times
    try:
        start_seconds = parse_time(start_time)
        end_seconds = parse_time(end_time)
    except ValueError as e:
        print(f"Error parsing time: {e}")
        sys.exit(1)
    
    # Calculate duration
    duration = end_seconds - start_seconds
    if duration <= 0:
        print(f"Error: End time must be after start time.")
        sys.exit(1)
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_trimmed.mp4"
    
    # Check if output file already exists
    if os.path.exists(output_file):
        response = input(f"Output file '{output_file}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Format times for ffmpeg
    start_time_formatted = format_time(start_seconds)
    duration_formatted = format_time(duration)
    
    print(f"Trimming video:")
    print(f"  Input: {input_file}")
    print(f"  Start: {start_time_formatted} ({start_seconds:.3f}s)")
    print(f"  End: {format_time(end_seconds)} ({end_seconds:.3f}s)")
    print(f"  Duration: {duration_formatted} ({duration:.3f}s)")
    print(f"  Output: {output_file}")
    print()
    
    # Build ffmpeg command
    # -ss: start time (seeking before input for faster processing)
    # -t: duration
    # -c:v libx264: H.264 video codec
    # -preset medium: encoding speed/quality balance
    # -crf 23: quality (lower = better quality, 18-28 is typical range)
    # -c:a aac: AAC audio codec
    # -movflags +faststart: enables web streaming (metadata at beginning)
    cmd = [
        'ffmpeg',
        '-ss', start_time_formatted,
        '-i', input_file,
        '-t', duration_formatted,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        '-y',  # Overwrite output file
        str(output_file)
    ]
    
    print("Running ffmpeg...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Successfully created: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg:")
        print(e.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Trim a .mov video file and convert to web-compatible .mp4 format.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s video.mov 00:00:10 00:01:30
  %(prog)s video.mov 10 90
  %(prog)s video.mov 00:00:10 00:01:30 output.mp4
  %(prog)s video.mov 1:30 2:45 output_trimmed.mp4
        """
    )
    
    parser.add_argument('input_file', help='Input .mov video file')
    parser.add_argument('start_time', help='Start time (HH:MM:SS, MM:SS, or seconds)')
    parser.add_argument('end_time', help='End time (HH:MM:SS, MM:SS, or seconds)')
    parser.add_argument('output_file', nargs='?', default=None,
                       help='Output .mp4 file (optional, defaults to input_filename_trimmed.mp4)')
    
    args = parser.parse_args()
    
    trim_video(args.input_file, args.start_time, args.end_time, args.output_file)


if __name__ == '__main__':
    main()

