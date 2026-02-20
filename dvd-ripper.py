#!/usr/bin/env python3
"""
DVD Ripper - Music DVD Content Extraction
Automates DVD ripping with configurable output formats (MP4, MKV, HEVC, Audio-only)
Uses HandBrake CLI (free, GPLv2) for extraction and conversion
"""

import os
import subprocess
import sys
import re
import shutil
from pathlib import Path

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
    """Output format configurations for HandBrake"""
    FORMATS = {
        '1': {
            'name': 'MP4 (H.264)',
            'extension': 'mp4',
            'encoder': 'x264',
            'format': 'av_mp4',
            'aencoder': 'av_aac',
            'description': 'Most compatible - works on all devices'
        },
        '2': {
            'name': 'MKV (H.264)',
            'extension': 'mkv',
            'encoder': 'x264',
            'format': 'av_mkv',
            'aencoder': 'flac24',
            'description': 'Best for multiple audio/subtitle tracks'
        },
        '3': {
            'name': 'MP4 (H.265/HEVC)',
            'extension': 'mp4',
            'encoder': 'x265',
            'format': 'av_mp4',
            'aencoder': 'av_aac',
            'description': 'Smaller files, modern devices only'
        },
        '4': {
            'name': 'Audio Only (FLAC)',
            'extension': 'flac',
            'encoder': None,
            'format': None,
            'aencoder': 'flac24',
            'description': 'Lossless audio extraction'
        },
        '5': {
            'name': 'Audio Only (MP3)',
            'extension': 'mp3',
            'encoder': None,
            'format': None,
            'aencoder': 'mp3',
            'description': 'Compressed audio extraction'
        }
    }

class QualityPreset:
    """Quality presets for HandBrake encoding"""
    PRESETS = {
        '1': {
            'name': 'High Quality (Larger files)',
            'quality': 18,
            'preset': 'slow',
            'audio_bitrate': '320',
            'hb_preset': 'HQ 480p30 Surround',
            'description': 'Best quality, larger file size'
        },
        '2': {
            'name': 'Balanced (Recommended)',
            'quality': 22,
            'preset': 'medium',
            'audio_bitrate': '256',
            'hb_preset': 'Fast 480p30',
            'description': 'Good quality with reasonable file size'
        },
        '3': {
            'name': 'Fast/Smaller (Lower quality)',
            'quality': 26,
            'preset': 'fast',
            'audio_bitrate': '192',
            'hb_preset': 'Very Fast 480p30',
            'description': 'Faster encoding, smaller files'
        }
    }

class DVDRipper:
    def __init__(self):
        self.dvd_device = "/dev/sr0"
        self.base_output_dir = "/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/DVD Rips"
        self.current_rip_dir = None
        self.selected_format = None
        self.selected_quality = None
        self.dvd_info = None
        self.titles = []
        
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
            'HandBrakeCLI': {'package': 'handbrake-cli', 'name': 'HandBrake CLI'},
            'ffmpeg': {'package': 'ffmpeg', 'name': 'FFmpeg'},
            'ffprobe': {'package': 'ffmpeg', 'name': 'FFprobe'},
            'lsdvd': {'package': 'lsdvd', 'name': 'lsdvd'}
        }
        
        missing = []
        missing_packages = []
        
        for cmd, info in dependencies.items():
            returncode, _, _ = self.run_command(f"which {cmd}")
            if returncode == 0:
                self.print_success(f"{info['name']} is installed")
            else:
                self.print_error(f"{info['name']} is NOT installed")
                missing.append(info['name'])
                if info['package'] not in missing_packages:
                    missing_packages.append(info['package'])
        
        # Check for libdvdcss (needed for encrypted DVDs)
        returncode, _, _ = self.run_command("ldconfig -p | grep libdvdcss")
        if returncode == 0:
            self.print_success("libdvdcss is installed (DVD decryption)")
        else:
            self.print_warning("libdvdcss not found - encrypted DVDs may not work")
            missing.append("libdvd-pkg")
            missing_packages.append("libdvd-pkg")
        
        if missing:
            self.print_warning(f"\nMissing: {', '.join(missing)}")
            print(f"\n{Colors.OKCYAN}To install on Debian/Ubuntu:{Colors.ENDC}")
            print(f"  sudo apt update")
            print(f"  sudo apt install {' '.join(missing_packages)}")
            print(f"  sudo dpkg-reconfigure libdvd-pkg  # Downloads libdvdcss")
            
            if self.yes_no_prompt("\nWould you like to attempt automatic installation?"):
                self.print_info("Installing missing packages...")
                self.run_command("apt update", show_output=True)
                
                for pkg in missing_packages:
                    self.print_info(f"Installing {pkg}...")
                    returncode, _, _ = self.run_command(f"apt install -y {pkg}", show_output=True)
                    if returncode != 0:
                        self.print_error(f"Failed to install {pkg}")
                
                # Configure libdvd-pkg if installed
                if "libdvd-pkg" in missing_packages:
                    self.print_info("Configuring libdvd-pkg (this downloads libdvdcss)...")
                    self.run_command("dpkg-reconfigure libdvd-pkg", show_output=True)
                
                self.print_success("Installation complete - please re-run the script")
                return False
            else:
                self.print_error("Cannot proceed without required packages")
                return False
        
        return True
    
    def check_dvd_inserted(self):
        """Check if a DVD is inserted"""
        self.print_header("Checking for DVD")
        
        # Try lsdvd first
        returncode, stdout, stderr = self.run_command(f"lsdvd {self.dvd_device} 2>&1", capture_output=True)
        
        combined = (stdout or "") + (stderr or "")
        if returncode != 0 or "cannot open" in combined.lower() or "no such file" in combined.lower():
            self.print_warning("No DVD detected in drive")
            input(f"{Colors.WARNING}Please insert a DVD and press Enter...{Colors.ENDC}")
            return self.check_dvd_inserted()  # Recursive check
        else:
            self.print_success("DVD detected!")
            return True
    
    def get_dvd_info(self):
        """Get DVD information using lsdvd and HandBrake"""
        self.print_header("Analyzing DVD")
        
        # Get basic info with lsdvd
        returncode, stdout, _ = self.run_command(f"lsdvd -x {self.dvd_device} 2>&1", capture_output=True)
        
        dvd_title = "Unknown DVD"
        self.titles = []
        
        if returncode == 0 and stdout:
            print(f"\n{Colors.OKCYAN}DVD Information:{Colors.ENDC}")
            
            # Parse lsdvd output
            for line in stdout.split('\n'):
                if 'Disc Title:' in line:
                    dvd_title = line.split(':', 1)[1].strip()
                    print(f"  Disc Title: {Colors.BOLD}{dvd_title}{Colors.ENDC}")
                elif line.strip().startswith('Title:'):
                    # Parse title info: "Title: 01, Length: 00:45:30.123 Chapters: 12, ..."
                    title_match = re.search(r'Title:\s*(\d+)', line)
                    length_match = re.search(r'Length:\s*([\d:\.]+)', line)
                    chapters_match = re.search(r'Chapters:\s*(\d+)', line)
                    
                    if title_match:
                        title_num = int(title_match.group(1))
                        length = length_match.group(1) if length_match else "Unknown"
                        chapters = int(chapters_match.group(1)) if chapters_match else 0
                        
                        self.titles.append({
                            'number': title_num,
                            'length': length,
                            'chapters': chapters
                        })
        
        self.dvd_info = {
            'title': dvd_title,
            'num_titles': len(self.titles)
        }
        
        # Get more detailed info with HandBrake
        self.print_info("\nScanning with HandBrake (this may take a moment)...")
        returncode, stdout, stderr = self.run_command(
            f'HandBrakeCLI --input {self.dvd_device} --title 0 --scan 2>&1',
            capture_output=True
        )
        
        combined = (stdout or "") + (stderr or "")
        
        # Parse HandBrake scan output
        if combined:
            # Look for title information in HandBrake output
            hb_titles = []
            current_title = None
            
            for line in combined.split('\n'):
                # Match: "+ title 1:"
                title_match = re.match(r'\s*\+\s*title\s+(\d+):', line)
                if title_match:
                    if current_title:
                        hb_titles.append(current_title)
                    current_title = {
                        'number': int(title_match.group(1)),
                        'duration': 'Unknown',
                        'chapters': 0
                    }
                
                # Match: "  + duration: 00:45:30"
                duration_match = re.search(r'duration:\s*([\d:]+)', line)
                if duration_match and current_title:
                    current_title['duration'] = duration_match.group(1)
                
                # Match: "  + chapters:"
                if '+ chapters:' in line.lower() and current_title:
                    # Count chapter lines that follow
                    pass
            
            if current_title:
                hb_titles.append(current_title)
            
            # Use HandBrake titles if we found more detail
            if hb_titles:
                self.titles = hb_titles
        
        # Display titles
        if self.titles:
            print(f"\n{Colors.OKCYAN}Titles found: {len(self.titles)}{Colors.ENDC}")
            for t in self.titles[:15]:  # Show first 15
                duration = t.get('duration') or t.get('length', 'Unknown')
                print(f"  Title {t['number']:2d}: {duration}")
            if len(self.titles) > 15:
                print(f"  ... and {len(self.titles) - 15} more titles")
        
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
        if self.selected_format and self.selected_format.get('encoder') is None:
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
    
    def rip_title_handbrake(self, title_num, output_name, track_num=None):
        """Rip a single title using HandBrake CLI"""
        
        # Build output filename
        if track_num:
            output_filename = f"{track_num:02d} - {output_name}.{self.selected_format['extension']}"
        else:
            output_filename = f"{output_name}.{self.selected_format['extension']}"
        
        output_path = os.path.join(self.current_rip_dir, output_filename)
        
        # Check if audio-only
        if self.selected_format.get('encoder') is None:
            # Use FFmpeg for audio extraction (more reliable for audio-only)
            return self.extract_audio_ffmpeg(title_num, output_path)
        
        # Build HandBrake command
        encoder = self.selected_format['encoder']
        format_type = self.selected_format['format']
        aencoder = self.selected_format['aencoder']
        quality = self.selected_quality['quality']
        preset = self.selected_quality['preset']
        audio_bitrate = self.selected_quality['audio_bitrate']
        
        cmd_parts = [
            'HandBrakeCLI',
            f'--input {self.dvd_device}',
            f'--title {title_num}',
            f'--output "{output_path}"',
            f'--format {format_type}',
            f'--encoder {encoder}',
            f'--quality {quality}',
            f'--encoder-preset {preset}',
            f'--aencoder {aencoder}',
            f'--ab {audio_bitrate}',
            '--all-audio',  # Include all audio tracks
            '--all-subtitles',  # Include all subtitles
            '--markers',  # Include chapter markers
        ]
        
        # Add HEVC-specific options for Apple compatibility
        if encoder == 'x265':
            cmd_parts.append('--encoder-tune fastdecode')
        
        cmd = ' '.join(cmd_parts)
        
        self.print_info(f"Ripping title {title_num} to {self.selected_format['name']}...")
        
        returncode, _, stderr = self.run_command(cmd, show_output=True)
        
        if returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            self.print_success(f"Completed: {output_filename} ({size_mb:.1f} MB)")
            return output_path
        else:
            self.print_error(f"Failed to rip title {title_num}")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            return None
    
    def extract_audio_ffmpeg(self, title_num, output_path):
        """Extract audio from DVD title using FFmpeg"""
        self.print_info(f"Extracting audio from title {title_num}...")
        
        # First, use HandBrake to extract to a temp MKV with audio
        temp_mkv = f"/tmp/dvd_audio_temp_{title_num}.mkv"
        
        # Extract with HandBrake first (handles DVD structure)
        cmd = f'HandBrakeCLI --input {self.dvd_device} --title {title_num} --output "{temp_mkv}" --format av_mkv --encoder x264 --quality 30 --encoder-preset ultrafast --aencoder copy'
        
        returncode, _, _ = self.run_command(cmd, show_output=True)
        
        if returncode != 0 or not os.path.exists(temp_mkv):
            self.print_error("Failed to extract title for audio processing")
            return None
        
        # Now extract audio with FFmpeg
        ext = self.selected_format['extension']
        
        if ext == 'flac':
            audio_cmd = f'ffmpeg -i "{temp_mkv}" -vn -acodec flac "{output_path}" -y'
        else:  # mp3
            bitrate = self.selected_quality['audio_bitrate']
            audio_cmd = f'ffmpeg -i "{temp_mkv}" -vn -acodec libmp3lame -ab {bitrate}k "{output_path}" -y'
        
        returncode, _, _ = self.run_command(audio_cmd, show_output=True)
        
        # Clean up temp file
        if os.path.exists(temp_mkv):
            os.remove(temp_mkv)
        
        if returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            self.print_success(f"Audio extracted: {os.path.basename(output_path)} ({size_mb:.1f} MB)")
            return output_path
        else:
            self.print_error("Audio extraction failed")
            return None
    
    def run_batch_mode(self):
        """Run in batch mode - process all titles automatically"""
        self.print_header("Batch Mode - Ripping All Titles")
        
        if not self.titles:
            self.print_error("No titles found on DVD")
            return False
        
        # Filter to main content (titles > 1 minute typically)
        main_titles = []
        for t in self.titles:
            duration = t.get('duration') or t.get('length', '00:00:00')
            # Parse duration to check if > 1 minute
            try:
                parts = duration.split(':')
                if len(parts) >= 2:
                    minutes = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 3 else int(parts[0])
                    if minutes >= 1:
                        main_titles.append(t)
            except:
                main_titles.append(t)  # Include if we can't parse
        
        if not main_titles:
            main_titles = self.titles
        
        self.print_info(f"Processing {len(main_titles)} title(s)...")
        
        converted = []
        for i, title in enumerate(main_titles, 1):
            title_num = title['number']
            duration = title.get('duration') or title.get('length', 'Unknown')
            
            self.print_info(f"\n[{i}/{len(main_titles)}] Title {title_num} ({duration})")
            
            output_name = f"Track {i:02d}"
            
            # Allow rename
            if self.yes_no_prompt(f"Rename '{output_name}'?"):
                output_name = self.get_input("Enter new name", output_name)
            
            result = self.rip_title_handbrake(title_num, output_name, track_num=i)
            if result:
                converted.append(result)
        
        return len(converted) > 0
    
    def run_selective_mode(self):
        """Run in selective mode - let user choose which titles to process"""
        self.print_header("Selective Mode")
        
        if not self.titles:
            self.print_error("No titles found on DVD")
            return False
        
        # Show titles
        print(f"\n{Colors.OKCYAN}Available titles:{Colors.ENDC}")
        for t in self.titles:
            duration = t.get('duration') or t.get('length', 'Unknown')
            print(f"  {t['number']:2d}. Duration: {duration}")
        
        # Let user select
        selected_str = self.get_input(
            f"\nEnter title numbers to rip (e.g., 1,2,3 or 'all')",
            "all"
        )
        
        if selected_str.lower() == 'all':
            selected_titles = self.titles
        else:
            try:
                selected_nums = [int(x.strip()) for x in selected_str.split(',')]
                selected_titles = [t for t in self.titles if t['number'] in selected_nums]
            except:
                self.print_warning("Invalid selection, processing all titles")
                selected_titles = self.titles
        
        if not selected_titles:
            self.print_error("No titles selected")
            return False
        
        self.print_info(f"\nProcessing {len(selected_titles)} selected title(s)...")
        
        converted = []
        for i, title in enumerate(selected_titles, 1):
            title_num = title['number']
            duration = title.get('duration') or title.get('length', 'Unknown')
            
            self.print_info(f"\n[{i}/{len(selected_titles)}] Title {title_num} ({duration})")
            
            output_name = self.get_input(f"Enter name for title {title_num}", f"Track {i:02d}")
            
            result = self.rip_title_handbrake(title_num, output_name, track_num=i)
            if result:
                converted.append(result)
        
        return len(converted) > 0
    
    def show_summary(self):
        """Show ripping summary"""
        self.print_header("Ripping Summary")
        
        if not self.current_rip_dir or not os.path.exists(self.current_rip_dir):
            self.print_warning("No output directory found")
            return
        
        # Find all output files
        extensions = ['mp4', 'mkv', 'flac', 'mp3']
        files = []
        for ext in extensions:
            files.extend(Path(self.current_rip_dir).glob(f"*.{ext}"))
        
        if not files:
            self.print_warning("No files were created")
            return
        
        total_size = 0
        print(f"{Colors.OKCYAN}Created files:{Colors.ENDC}")
        for f in sorted(files):
            size_mb = f.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"  ✓ {f.name} ({size_mb:.1f} MB)")
        
        print(f"\n{Colors.OKGREEN}Total: {len(files)} file(s), {total_size:.1f} MB{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Location: {self.current_rip_dir}{Colors.ENDC}")
    
    def eject_dvd(self):
        """Eject the DVD"""
        self.print_info("Ejecting DVD...")
        self.run_command(f"eject {self.dvd_device}")
        self.print_success("DVD ejected")
    
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
            self.show_summary()
        
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
║       Powered by HandBrake CLI (Free & Open Source)       ║
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
