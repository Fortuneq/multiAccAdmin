"""
Video generator service using FFmpeg.
Handles video processing, audio mixing, filters, and subtitles.
"""
import ffmpeg
from pathlib import Path
from typing import Optional
import uuid
from datetime import datetime

from app.config import get_settings

settings = get_settings()


class VideoGenerator:
    """
    Service for video generation and processing using FFmpeg.

    Provides methods for:
    - Adding audio to video
    - Applying visual filters
    - Adding subtitles
    - Compositing final video with all effects
    """

    def __init__(self):
        self.output_dir = Path(settings.UPLOAD_DIR) / "projects"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_output_path(self, prefix: str = "video") -> str:
        """Generate unique output file path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{prefix}_{timestamp}_{unique_id}.mp4"
        return str(self.output_dir / filename)

    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        volume: float = 1.0
    ) -> str:
        """
        Add audio track to video.

        Args:
            video_path: Path to source video file
            audio_path: Path to audio file
            volume: Audio volume multiplier (0.0 to 2.0)

        Returns:
            Path to output video file

        Raises:
            Exception: If FFmpeg processing fails
        """
        output_path = self._generate_output_path("audio_mixed")

        try:
            video = ffmpeg.input(video_path)
            audio = ffmpeg.input(audio_path)

            # Adjust audio volume
            audio = audio.filter('volume', volume)

            # Combine video and audio
            output = ffmpeg.output(
                video,
                audio,
                output_path,
                vcodec='libx264',
                acodec='aac',
                strict='experimental',
                shortest=None  # Use shortest stream duration
            )

            ffmpeg.run(output, overwrite_output=True, capture_stdout=True, capture_stderr=True)

            return output_path

        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"Failed to add audio: {error_message}")

    def apply_filter(
        self,
        video_path: str,
        filter_type: str
    ) -> str:
        """
        Apply visual filter to video.

        Args:
            video_path: Path to source video file
            filter_type: Filter type (cinematic, bright, cyberpunk, vintage, warm, cool)

        Returns:
            Path to output video file

        Raises:
            Exception: If FFmpeg processing fails
        """
        output_path = self._generate_output_path(f"filtered_{filter_type}")

        # Define filter presets
        filters = {
            "cinematic": "eq=contrast=1.2:brightness=0.05:saturation=0.8,vignette=PI/4",
            "bright": "eq=brightness=0.15:contrast=1.1:saturation=1.2",
            "cyberpunk": "eq=contrast=1.3:saturation=1.5,colorchannelmixer=rr=1:rb=0.3:br=0.2:bb=1:bg=0.2",
            "vintage": "curves=vintage,colorbalance=rs=0.1:gs=-0.05:bs=-0.1",
            "warm": "colortemperature=temperature=7000,eq=saturation=1.1",
            "cool": "colortemperature=temperature=3000,eq=saturation=1.1",
            "none": None
        }

        filter_string = filters.get(filter_type.lower())

        try:
            video = ffmpeg.input(video_path)

            if filter_string:
                video = video.filter_multi_output(filter_string)

            output = ffmpeg.output(
                video,
                output_path,
                vcodec='libx264',
                acodec='copy'
            )

            ffmpeg.run(output, overwrite_output=True, capture_stdout=True, capture_stderr=True)

            return output_path

        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"Failed to apply filter: {error_message}")

    def add_subtitles(
        self,
        video_path: str,
        text: str,
        uniquify: bool = False
    ) -> str:
        """
        Add subtitles to video.

        Args:
            video_path: Path to source video file
            text: Subtitle text content
            uniquify: Apply unique styling to subtitles

        Returns:
            Path to output video file

        Raises:
            Exception: If FFmpeg processing fails
        """
        output_path = self._generate_output_path("subtitled")

        # Create temporary subtitle file (SRT format)
        srt_path = self.output_dir / f"subtitle_{uuid.uuid4().hex}.srt"

        # Write SRT file
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:10:00,000\n")
            f.write(f"{text}\n")

        try:
            video = ffmpeg.input(video_path)

            # Subtitle styling
            if uniquify:
                # Unique styling: yellow, bold, border
                subtitle_style = "Fontsize=24,PrimaryColour=&H00FFFF,Bold=1,BorderStyle=1"
            else:
                # Standard styling: white, centered
                subtitle_style = "Fontsize=20,PrimaryColour=&HFFFFFF"

            # Add subtitles using subtitles filter
            video = video.filter(
                'subtitles',
                str(srt_path),
                force_style=subtitle_style
            )

            output = ffmpeg.output(
                video,
                output_path,
                vcodec='libx264',
                acodec='copy'
            )

            ffmpeg.run(output, overwrite_output=True, capture_stdout=True, capture_stderr=True)

            # Clean up subtitle file
            srt_path.unlink(missing_ok=True)

            return output_path

        except ffmpeg.Error as e:
            srt_path.unlink(missing_ok=True)  # Clean up on error
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"Failed to add subtitles: {error_message}")

    def composite_video(
        self,
        video_path: str,
        audio_path: Optional[str] = None,
        subtitle_text: Optional[str] = None,
        volume: int = 100,
        filter_type: str = "none",
        uniquify: bool = False
    ) -> str:
        """
        Composite video with all effects (audio, filters, subtitles).

        This is the main processing pipeline that combines all effects.

        Args:
            video_path: Path to source video file
            audio_path: Path to audio file (optional)
            subtitle_text: Subtitle text (optional)
            volume: Audio volume (0-100)
            filter_type: Visual filter type
            uniquify: Apply unique subtitle styling

        Returns:
            Path to final output video file

        Raises:
            Exception: If any processing step fails
        """
        current_video = video_path

        try:
            # Step 1: Apply visual filter if specified
            if filter_type and filter_type.lower() != "none":
                current_video = self.apply_filter(current_video, filter_type)

            # Step 2: Add audio if provided
            if audio_path:
                volume_multiplier = volume / 100.0  # Convert 0-100 to 0.0-1.0
                current_video = self.add_audio(current_video, audio_path, volume_multiplier)

            # Step 3: Add subtitles if provided
            if subtitle_text:
                current_video = self.add_subtitles(current_video, subtitle_text, uniquify)

            return current_video

        except Exception as e:
            raise Exception(f"Video composition failed: {str(e)}")

    def get_video_info(self, video_path: str) -> dict:
        """
        Get video metadata using FFprobe.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary with video metadata (duration, resolution, codec, etc.)
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None
            )

            if video_stream:
                return {
                    'duration': float(probe['format'].get('duration', 0)),
                    'width': int(video_stream.get('width', 0)),
                    'height': int(video_stream.get('height', 0)),
                    'codec': video_stream.get('codec_name', 'unknown'),
                    'fps': eval(video_stream.get('r_frame_rate', '0/1')),
                    'size': int(probe['format'].get('size', 0))
                }

            return {}

        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")
