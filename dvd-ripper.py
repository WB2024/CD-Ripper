#!/usr/bin/env python3
"""
DVD Ripper - Music DVD Content Extraction
Automates DVD ripping with configurable output formats (MP4, MKV, HEVC, Audio-only)
Uses MakeMKV for extraction and FFmpeg for conversion
"""

import os
import subprocess
import sys
import time
import json
import shutil
from pathlib import Path
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class OutputFormat:
    """Output format configurations"""
    FORMATS = {
        '1': {
            'name': 'MP4 (H.264)',
            'extension': 'mp4',
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'container': 'mp4',
            'description': 'Most compatible - works on all devices'
        },
        '2': {
            'name': 'MKV (H.264)',
            'extension': 'mkv',
            'video_codec': 'libx264',
            'audio_codec': 'flac',
            'container': 'matroska',
            'description': 'Best for multiple audio/subtitle tracks'
        },
        '3': {
            'name': 'MP4 (H.265/HEVC)',
            'extension': 'mp4',
            'video_codec': 'libx265',
            'audio_codec': 'aac',
            'container': 'mp4',
            'description': 'Smaller files, modern devices only'
        },
        '4': {
            'name': 'Audio Only (FLAC)',
            'extension': 'flac',
            'video_codec': None,
            'audio_codec': 'flac',
            'container': 'flac',
            'description': 'Lossless audio extraction'
        },
        '5': {
            'name': 'Audio Only (MP3)',
            'extension': 'mp3',
            'video_codec': None,
            'audio_codec': 'libmp3lame',
            'container': 'mp3',
            'description': 'Compressed audio extraction'
        }
    }

class QualityPreset:
    """Quality presets for video encoding"""
    PRESETS = {
        '1': {
            'name': 'High Quality (Larger files)',
            'crf': 18,
            'preset': 'slow',
            'audio_bitrate': '320k',
            'description': 'Best quality, larger file size'
        },
        '2': {
            'name': 'Balanced (Recommended)',
            'crf': 22,
            'preset': 'medium',
            'audio_bitrate': '256k',
            'description': 'Good quality with reasonable file size'
        },
        '3': {
            'name': 'Fast/Smaller (Lower quality)',
            'crf': 26,
            'preset': 'fast',
            'audio_bitrate': '192k',
            'description': 'Faster encoding, smaller files'
        }
    }

class DVDRipper:
    def __init__(self):
        self.dvd_device = "/dev/sr0"
        self.base_output_dir = "/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/DVD Rips"
        self.temp_dir = "/tmp/dvd-ripper"
        self.current_rip_dir = None
        self.selected_format = None
        self.selected_quality = None
        self.dvd_info = None
        
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")
    
    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    def run_command(self, command, show_output=False, capture_output=False):
        """Run a shell command"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.returncode, result.stdout, result.stderr
            elif show_output:
                result = subprocess.run(command, shell=True)
                return result.returncode, None, None
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.returncode, result.stdout, result.stderr
        except Exception as e:
            self.print_error(f"Command failed: {e}")
            return 1, None, str(e)
    
    def yes_no_prompt(self, question):
        """Ask a yes/no question"""
        while True:
            response = input(f"{Colors.OKBLUE}{question} (y/n): {Colors.ENDC}").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                self.print_warning("Please answer 'y' or 'n'")
    
    def get_input(self, prompt, default=None):
        """Get user input with optional default"""
        if default:
            response = input(f"{Colors.OKBLUE}{prompt} [{default}]: {Colors.ENDC}").strip()
            return response if response else default
        else:
            return input(f"{Colors.OKBLUE}{prompt}: {Colors.ENDC}").strip()
    
    def select_option(self, prompt, options):
        """Display options and get user selection"""
        print(f"\n{Colors.OKCYAN}{prompt}{Colors.ENDC}\n")
        for key, option in options.items():
            print(f"  {Colors.BOLD}{key}{Colors.ENDC}. {option['name']}")
            print(f"     {Colors.OKCYAN}{option['description']}{Colors.ENDC}")
        
        while True:
            choice = input(f"\n{Colors.OKBLUE}Select option (1-{len(options)}): {Colors.ENDC}").strip()
            if choice in options:
                return options[choice]
            self.print_warning(f"Please enter a number between 1 and {len(options)}")
    
    def fix_permissions(self, directory=None):
        """Set permissions to 777 for all files and folders in the ripped directory"""
        if directory is None:
            directory = self.base_output_dir
        
        self.print_info(f"Setting permissions for: {directory}")
        returncode, _, _ = self.run_command(f"chmod -R 777 '{directory}'")
        
        if returncode == 0:
            self.print_success("Permissions set successfully (777)")
        else:
            self.print_warning("Failed to set permissions (you may need to do this manually)")
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        self.print_header("Checking Dependencies")
        
        dependencies = {
            'makemkvcon': {'package': 'makemkv-bin makemkv-oss', 'name': 'MakeMKV'},
            'ffmpeg': {'package': 'ffmpeg', 'name': 'FFmpeg'},
            'ffprobe': {'package': 'ffmpeg', 'name': 'FFprobe'},
            'lsdvd': {'package': 'lsdvd', 'name': 'lsdvd'}
        }
        
        missing = []
        for cmd, info in dependencies.items():
            returncode, _, _ = self.run_command(f"which {cmd}")
            if returncode == 0:
                self.print_success(f"{info['name']} is installed")
            else:
                self.print_error(f"{info['name']} is NOT installed")
                if info['package'] not in missing:
                    missing.append(info['package'])
        
        if missing:
            self.print_warning(f"\nMissing packages: {', '.join(missing)}")
            print(f"\n{Colors.OKCYAN}To install MakeMKV on Ubuntu/Debian:{Colors.ENDC}")
            print("  sudo add-apt-repository ppa:heyarje/makemkv-beta")
            print("  sudo apt update")
            print("  sudo apt install makemkv-bin makemkv-oss lsdvd ffmpeg")
            print(f"\n{Colors.OKCYAN}For other distributions, visit:{Colors.ENDC}")
            print("  https://www.makemkv.com/download/")
            
            if not self.yes_no_prompt("\nWould you like to attempt automatic installation?"):
                self.print_error("Cannot proceed without required packages")
                return False
            
            # Try to install
            self.print_info("Attempting to install missing packages...")
            
            # Add PPA for MakeMKV
            self.run_command("add-apt-repository -y ppa:heyarje/makemkv-beta 2>/dev/null", show_output=True)
            self.run_command("apt update", show_output=True)
            
            for pkg in missing:
                self.print_info(f"Installing {pkg}...")
                returncode, _, _ = self.run_command(f"apt install -y {pkg}", show_output=True)
                if returncode != 0:
                    self.print_error(f"Failed to install {pkg}")
                    return False
            
            self.print_success("Packages installed successfully")
        
        return True
    
    def check_dvd_inserted(self):
        """Check if a DVD is inserted"""
        self.print_header("Checking for DVD")
        
        # Try lsdvd first
        returncode, stdout, _ = self.run_command(f"lsdvd {self.dvd_device} 2>&1", capture_output=True)
        
        if returncode != 0 or "cannot open" in stdout.lower() or "no such file" in stdout.lower():
            self.print_warning("No DVD detected in drive")
            input(f"{Colors.WARNING}Please insert a DVD and press Enter...{Colors.ENDC}")
            return self.check_dvd_inserted()  # Recursive check
        else:
            self.print_success("DVD detected!")
            return True
    
    def get_dvd_info(self):
        """Get DVD information using lsdvd and makemkvcon"""
        self.print_header("Analyzing DVD")
        
        # Get basic info with lsdvd
        returncode, stdout, _ = self.run_command(f"lsdvd -x {self.dvd_device} 2>&1", capture_output=True)
        
        if returncode == 0:
            print(f"\n{Colors.OKCYAN}DVD Information:{Colors.ENDC}")
            
            # Parse lsdvd output
            dvd_title = "Unknown DVD"
            titles = []
            
            for line in stdout.split('\n'):
                if 'Disc Title:' in line:
                    dvd_title = line.split(':', 1)[1].strip()
                    print(f"  Disc Title: {Colors.BOLD}{dvd_title}{Colors.ENDC}")
                elif line.startswith('Title:'):
                    titles.append(line)
            
            if titles:
                print(f"\n{Colors.OKCYAN}Titles found: {len(titles)}{Colors.ENDC}")
                for title in titles[:10]:  # Show first 10
                    print(f"  {title}")
                if len(titles) > 10:
                    print(f"  ... and {len(titles) - 10} more titles")
            
            self.dvd_info = {
                'title': dvd_title,
                'num_titles': len(titles),
                'raw_output': stdout
            }
        
        # Also get MakeMKV info
        self.print_info("\nScanning with MakeMKV (this may take a moment)...")
        returncode, stdout, _ = self.run_command(f"makemkvcon -r info disc:0 2>&1", capture_output=True)
        
        if returncode == 0 and stdout:
            # Parse MakeMKV output for more details
            for line in stdout.split('\n'):
                if 'TINFO' in line and ',2,' in line:  # Title name
                    parts = line.split(',')
                    if len(parts) >= 4:
                        title_name = parts[3].strip('"')
                        if title_name and 'title' not in title_name.lower():
                            print(f"  Found content: {title_name}")
            
            self.dvd_info['makemkv_output'] = stdout
        
        return self.dvd_info
    
    def select_output_format(self):
        """Let user select output format"""
        self.print_header("Select Output Format")
        self.selected_format = self.select_option(
            "Choose your preferred output format:",
            OutputFormat.FORMATS
        )
        self.print_success(f"Selected: {self.selected_format['name']}")
        return self.selected_format
    
    def select_quality_preset(self):
        """Let user select quality preset"""
        # Only ask for quality if not audio-only
        if self.selected_format and self.selected_format.get('video_codec') is None:
            self.print_info("Audio-only format selected - using best quality")
            self.selected_quality = QualityPreset.PRESETS['1']
            return self.selected_quality
        
        self.print_header("Select Quality Preset")
        self.selected_quality = self.select_option(
            "Choose your preferred quality:",
            QualityPreset.PRESETS
        )
        self.print_success(f"Selected: {self.selected_quality['name']}")
        return self.selected_quality
    
    def get_output_name(self):
        """Get the output name from user"""
        self.print_header("Output Settings")
        
        # Suggest name from DVD info
        default_name = "DVD_Rip"
        if self.dvd_info and self.dvd_info.get('title'):
            default_name = self.dvd_info['title'].replace(' ', '_').replace('/', '-')
        
        artist = self.get_input("Enter Artist/Band name", "Unknown Artist")
        album = self.get_input("Enter Album/DVD title", default_name)
        
        # Create output directory
        self.current_rip_dir = os.path.join(self.base_output_dir, artist, album)
        os.makedirs(self.current_rip_dir, exist_ok=True)
        
        self.print_success(f"Output directory: {self.current_rip_dir}")
        return artist, album
    
    def rip_dvd_with_makemkv(self):
        """Extract DVD content using MakeMKV"""
        self.print_header("Extracting DVD Content")
        
        # Create temp directory
        os.makedirs(self.temp_dir, exist_ok=True)
        
        self.print_info("Extracting titles with MakeMKV...")
        self.print_info("This may take several minutes depending on DVD size...")
        
        # Use MakeMKV to extract all titles to MKV
        cmd = f'makemkvcon mkv disc:0 all "{self.temp_dir}" --progress=-same'
        returncode, _, _ = self.run_command(cmd, show_output=True)
        
        if returncode != 0:
            self.print_error("MakeMKV extraction failed")
            return False
        
        # Check what was extracted
        extracted_files = list(Path(self.temp_dir).glob("*.mkv"))
        
        if not extracted_files:
            self.print_error("No files were extracted")
            return False
        
        self.print_success(f"Extracted {len(extracted_files)} title(s)")
        for f in extracted_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.1f} MB)")
        
        return extracted_files
    
    def get_video_duration(self, input_file):
        """Get video duration using ffprobe"""
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        returncode, stdout, _ = self.run_command(cmd, capture_output=True)
        if returncode == 0 and stdout:
            try:
                return float(stdout.strip())
            except:
                pass
        return None
    
    def convert_file(self, input_file, output_name, track_num=None):
        """Convert extracted file to selected format"""
        # Build output filename
        if track_num:
            output_filename = f"{track_num:02d} - {output_name}.{self.selected_format['extension']}"
        else:
            output_filename = f"{output_name}.{self.selected_format['extension']}"
        
        output_path = os.path.join(self.current_rip_dir, output_filename)
        
        # Build FFmpeg command based on format
        if self.selected_format.get('video_codec') is None:
            # Audio-only extraction
            if self.selected_format['audio_codec'] == 'flac':
                cmd = f'ffmpeg -i "{input_file}" -vn -acodec flac "{output_path}" -y'
            else:
                cmd = f'ffmpeg -i "{input_file}" -vn -acodec {self.selected_format["audio_codec"]} -ab {self.selected_quality["audio_bitrate"]} "{output_path}" -y'
        else:
            # Video conversion
            video_codec = self.selected_format['video_codec']
            audio_codec = self.selected_format['audio_codec']
            crf = self.selected_quality['crf']
            preset = self.selected_quality['preset']
            audio_bitrate = self.selected_quality['audio_bitrate']
            
            # Add HEVC-specific options
            if video_codec == 'libx265':
                codec_opts = f'-c:v {video_codec} -crf {crf} -preset {preset} -tag:v hvc1'
            else:
                codec_opts = f'-c:v {video_codec} -crf {crf} -preset {preset}'
            
            # Handle audio
            if audio_codec == 'flac':
                audio_opts = '-c:a flac'
            elif audio_codec == 'aac':
                audio_opts = f'-c:a aac -b:a {audio_bitrate}'
            else:
                audio_opts = f'-c:a {audio_codec} -b:a {audio_bitrate}'
            
            cmd = f'ffmpeg -i "{input_file}" {codec_opts} {audio_opts} "{output_path}" -y'
        
        self.print_info(f"Converting to {self.selected_format['name']}...")
        
        # Get duration for progress estimation
        duration = self.get_video_duration(input_file)
        if duration:
            self.print_info(f"Duration: {int(duration // 60)}m {int(duration % 60)}s")
        
        returncode, _, stderr = self.run_command(cmd, show_output=True)
        
        if returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            self.print_success(f"Converted: {output_filename} ({size_mb:.1f} MB)")
            return output_path
        else:
            self.print_error(f"Conversion failed for {output_name}")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            return None
    
    def convert_all_titles(self, extracted_files):
        """Convert all extracted titles"""
        self.print_header("Converting Titles")
        
        converted = []
        total = len(extracted_files)
        
        for i, mkv_file in enumerate(extracted_files, 1):
            self.print_info(f"\nProcessing title {i}/{total}: {mkv_file.name}")
            
            # Get a nice output name
            base_name = mkv_file.stem
            # Try to make it nicer
            if base_name.startswith('title'):
                output_name = f"Track {i:02d}"
            else:
                output_name = base_name.replace('_', ' ').title()
            
            # Allow user to rename
            if self.yes_no_prompt(f"Rename '{output_name}'?"):
                output_name = self.get_input("Enter new name", output_name)
            
            result = self.convert_file(str(mkv_file), output_name, track_num=i)
            if result:
                converted.append(result)
        
        return converted
    
    def cleanup_temp(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            self.print_info("Cleaning up temporary files...")
            try:
                shutil.rmtree(self.temp_dir)
                self.print_success("Temporary files removed")
            except Exception as e:
                self.print_warning(f"Could not remove temp files: {e}")
    
    def eject_dvd(self):
        """Eject the DVD"""
        self.print_info("Ejecting DVD...")
        self.run_command(f"eject {self.dvd_device}")
        self.print_success("DVD ejected")
    
    def run_batch_mode(self):
        """Run in batch mode - process all titles automatically"""
        self.print_header("Batch Mode")
        
        # Rip with MakeMKV
        extracted_files = self.rip_dvd_with_makemkv()
        if not extracted_files:
            return False
        
        # Convert all
        converted = self.convert_all_titles(extracted_files)
        
        # Cleanup
        if self.yes_no_prompt("Remove temporary MKV files?"):
            self.cleanup_temp()
        
        return len(converted) > 0
    
    def run_selective_mode(self):
        """Run in selective mode - let user choose which titles to process"""
        self.print_header("Selective Mode")
        
        # Rip with MakeMKV
        extracted_files = self.rip_dvd_with_makemkv()
        if not extracted_files:
            return False
        
        # Show titles and let user select
        print(f"\n{Colors.OKCYAN}Extracted titles:{Colors.ENDC}")
        for i, f in enumerate(extracted_files, 1):
            size_mb = f.stat().st_size / (1024 * 1024)
            duration = self.get_video_duration(str(f))
            dur_str = f"{int(duration // 60)}m {int(duration % 60)}s" if duration else "Unknown"
            print(f"  {i}. {f.name} ({size_mb:.1f} MB, {dur_str})")
        
        # Let user select
        selected_indices = self.get_input(
            f"\nEnter title numbers to convert (e.g., 1,2,3 or 'all')",
            "all"
        )
        
        if selected_indices.lower() == 'all':
            files_to_convert = extracted_files
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selected_indices.split(',')]
                files_to_convert = [extracted_files[i] for i in indices if 0 <= i < len(extracted_files)]
            except:
                self.print_warning("Invalid selection, processing all titles")
                files_to_convert = extracted_files
        
        # Convert selected
        converted = []
        for i, mkv_file in enumerate(files_to_convert, 1):
            self.print_info(f"\nProcessing: {mkv_file.name}")
            
            output_name = self.get_input(f"Enter name for this track", f"Track {i:02d}")
            result = self.convert_file(str(mkv_file), output_name, track_num=i)
            if result:
                converted.append(result)
        
        # Cleanup
        if self.yes_no_prompt("Remove temporary MKV files?"):
            self.cleanup_temp()
        
        return len(converted) > 0
    
    def show_summary(self, converted_files):
        """Show ripping summary"""
        self.print_header("Ripping Summary")
        
        if not converted_files:
            self.print_warning("No files were converted")
            return
        
        total_size = 0
        print(f"{Colors.OKCYAN}Converted files:{Colors.ENDC}")
        for f in converted_files:
            if os.path.exists(f):
                size_mb = os.path.getsize(f) / (1024 * 1024)
                total_size += size_mb
                print(f"  ✓ {os.path.basename(f)} ({size_mb:.1f} MB)")
        
        print(f"\n{Colors.OKGREEN}Total: {len(converted_files)} file(s), {total_size:.1f} MB{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Location: {self.current_rip_dir}{Colors.ENDC}")
    
    def run(self):
        """Main workflow"""
        self.print_header("DVD Ripper - Music DVD Content Extraction")
        
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Check for DVD
        if not self.check_dvd_inserted():
            return
        
        # Get DVD info
        self.get_dvd_info()
        
        # Select output format
        self.select_output_format()
        
        # Select quality
        self.select_quality_preset()
        
        # Get output name/location
        self.get_output_name()
        
        # Ask to proceed
        if not self.yes_no_prompt("\nWould you like to proceed with ripping this DVD?"):
            self.print_info("Operation cancelled")
            return
        
        # Choose mode
        print(f"\n{Colors.OKCYAN}Select ripping mode:{Colors.ENDC}")
        print(f"  1. Batch Mode - Rip all titles automatically")
        print(f"  2. Selective Mode - Choose which titles to rip")
        
        mode = self.get_input("Select mode (1/2)", "1")
        
        if mode == "2":
            success = self.run_selective_mode()
        else:
            success = self.run_batch_mode()
        
        if success:
            # Fix permissions
            self.fix_permissions(self.current_rip_dir)
            
            # Show summary
            converted_files = list(Path(self.current_rip_dir).glob(f"*.{self.selected_format['extension']}"))
            self.show_summary([str(f) for f in converted_files])
        
        # Eject
        if self.yes_no_prompt("\nWould you like to eject the DVD?"):
            self.eject_dvd()
        
        self.print_header("Ripping Complete!")
        
        if success:
            self.print_success("All operations completed successfully")
        else:
            self.print_warning("Some operations may have failed")
        
        if self.yes_no_prompt("\nWould you like to rip another DVD?"):
            print("\n" * 2)
            self.run()

def main():
    """Entry point"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║              DVD Ripper - Music DVD Edition               ║
║          Extract & Convert DVD Content Easily             ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)
    
    try:
        ripper = DVDRipper()
        ripper.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
