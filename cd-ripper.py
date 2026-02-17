#!/usr/bin/env python3
"""
Enhanced CD Ripper with Audio and Data Extraction
Automates CD ripping to FLAC with metadata and enhanced content extraction
"""

import os
import subprocess
import sys
import time
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

class CDRipper:
    def __init__(self):
        self.cd_device = "/dev/sr0"
        self.base_output_dir = "/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/CD Rips"
        self.mount_point = "/mnt/cdrom-data"
        self.current_rip_dir = None
        
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
            'abcde': 'abcde',
            'cdparanoia': 'cdparanoia',
            'flac': 'flac',
            'ffmpeg': 'ffmpeg',
            'cdrdao': 'cdrdao'
        }
        
        missing = []
        for name, package in dependencies.items():
            returncode, _, _ = self.run_command(f"which {name}")
            if returncode == 0:
                self.print_success(f"{name} is installed")
            else:
                self.print_error(f"{name} is NOT installed")
                missing.append(package)
        
        if missing:
            self.print_warning(f"\nMissing packages: {', '.join(missing)}")
            if self.yes_no_prompt("Would you like to install missing packages now?"):
                self.print_info("Installing packages...")
                returncode, _, _ = self.run_command(f"apt update && apt install -y {' '.join(missing)}", show_output=True)
                if returncode == 0:
                    self.print_success("Packages installed successfully")
                else:
                    self.print_error("Failed to install packages")
                    return False
            else:
                self.print_error("Cannot proceed without required packages")
                return False
        
        return True
    
    def check_cd_inserted(self):
        """Check if a CD is inserted"""
        self.print_header("Checking for CD")
        
        returncode, stdout, _ = self.run_command(f"cdrdao disk-info --device {self.cd_device}", capture_output=True)
        
        if returncode != 0 or "no disc" in stdout.lower():
            self.print_warning("No CD detected in drive")
            input(f"{Colors.WARNING}Please insert a CD and press Enter...{Colors.ENDC}")
            return self.check_cd_inserted()  # Recursive check
        else:
            self.print_success("CD detected!")
            return True
    
    def get_cd_info(self):
        """Get CD session and track information"""
        self.print_header("Analyzing CD")
        
        # Get session info
        returncode, stdout, _ = self.run_command(f"cdrdao disk-info --device {self.cd_device}", capture_output=True)
        
        sessions = 1
        for line in stdout.split('\n'):
            if 'Sessions' in line:
                try:
                    sessions = int(line.split(':')[-1].strip())
                except:
                    pass
        
        self.print_info(f"Sessions found: {sessions}")
        
        # Get track info
        returncode, stdout, _ = self.run_command(f"cdparanoia -Q 2>&1", capture_output=True)
        print(f"\n{Colors.OKCYAN}{stdout}{Colors.ENDC}")
        
        return sessions
    
    def rip_audio(self):
        """Rip audio tracks using abcde"""
        self.print_header("Ripping Audio Tracks")
        
        self.print_info("Starting abcde - follow the prompts for metadata...")
        self.print_info("You can edit artist, album, and track names when prompted")
        
        returncode, _, _ = self.run_command(f"abcde -d {self.cd_device}", show_output=True)
        
        if returncode == 0:
            self.print_success("Audio ripping completed!")
            
            # Find and store the ripped directory
            self.current_rip_dir = self.find_latest_rip_directory()
            
            # Fix permissions on the newly created directory
            if self.current_rip_dir:
                self.fix_permissions(self.current_rip_dir)
            
            return True
        else:
            self.print_error("Audio ripping failed")
            return False
    
    def find_latest_rip_directory(self):
        """Find the most recently created directory in the output folder"""
        try:
            base_path = Path(self.base_output_dir)
            
            # Get all directories, sort by modification time
            dirs = []
            for artist_dir in base_path.iterdir():
                if artist_dir.is_dir():
                    for album_dir in artist_dir.iterdir():
                        if album_dir.is_dir():
                            dirs.append(album_dir)
            
            if dirs:
                latest = max(dirs, key=lambda x: x.stat().st_mtime)
                return str(latest)
            return None
        except Exception as e:
            self.print_error(f"Could not find rip directory: {e}")
            return None
    
    def extract_enhanced_content(self, output_dir=None):
        """Extract enhanced CD content from second session"""
        self.print_header("Extracting Enhanced Content")
        
        # Determine output directory
        if not output_dir:
            output_dir = self.current_rip_dir if self.current_rip_dir else self.find_latest_rip_directory()
            if not output_dir:
                output_dir = input(f"{Colors.OKBLUE}Enter the full path to save enhanced content: {Colors.ENDC}").strip()
        
        enhanced_dir = os.path.join(output_dir, "Enhanced Content")
        
        # Create mount point if needed
        returncode, _, _ = self.run_command(f"mkdir -p {self.mount_point}")
        
        # Try mounting session 2
        self.print_info("Attempting to mount data session...")
        returncode, _, _ = self.run_command(f"mount -t iso9660 -o session=1,ro {self.cd_device} {self.mount_point}")
        
        if returncode != 0:
            self.print_warning("Failed to mount with session=1, trying session=2...")
            returncode, _, _ = self.run_command(f"mount -t iso9660 -o session=2,ro {self.cd_device} {self.mount_point}")
        
        if returncode != 0:
            self.print_warning("Failed to mount data session, trying without session option...")
            returncode, _, _ = self.run_command(f"mount -t iso9660 -o ro {self.cd_device} {self.mount_point}")
        
        if returncode != 0:
            self.print_error("Could not mount enhanced content - this may not be an enhanced CD")
            return False
        
        # Check what's mounted
        self.print_info("Checking mounted content...")
        returncode, stdout, _ = self.run_command(f"ls -lh {self.mount_point}", capture_output=True)
        
        if returncode == 0 and stdout.strip():
            print(f"\n{Colors.OKCYAN}Found content:{Colors.ENDC}")
            print(stdout)
            
            # Create output directory
            self.run_command(f"mkdir -p '{enhanced_dir}'")
            
            # Copy all content
            self.print_info("Copying enhanced content...")
            returncode, _, _ = self.run_command(f"cp -rv {self.mount_point}/* '{enhanced_dir}/'", show_output=True)
            
            # Unmount
            self.run_command(f"umount {self.mount_point}")
            
            if returncode == 0:
                self.print_success(f"Enhanced content saved to: {enhanced_dir}")
                
                # Fix permissions on enhanced content
                self.fix_permissions(enhanced_dir)
                
                # Check for videos to convert
                self.convert_videos(enhanced_dir)
                return True
            else:
                self.print_error("Failed to copy enhanced content")
                self.run_command(f"umount {self.mount_point}")
                return False
        else:
            self.print_warning("No additional content found in data session")
            self.run_command(f"umount {self.mount_point}")
            return False
    
    def convert_videos(self, enhanced_dir):
        """Convert video files to MP4"""
        self.print_header("Checking for Videos to Convert")
        
        video_extensions = ['.flv', '.mov', '.avi', '.wmv', '.mpg', '.mpeg']
        videos_found = []
        
        for file in os.listdir(enhanced_dir):
            file_path = os.path.join(enhanced_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in video_extensions:
                    videos_found.append((file_path, file))
        
        if not videos_found:
            self.print_info("No videos found to convert")
            return
        
        self.print_info(f"Found {len(videos_found)} video file(s)")
        for _, filename in videos_found:
            print(f"  - {filename}")
        
        if not self.yes_no_prompt("\nWould you like to convert these videos to MP4?"):
            return
        
        for video_path, video_filename in videos_found:
            self.print_info(f"Converting {video_filename}...")
            
            # Create output filename
            base_name = os.path.splitext(video_filename)[0]
            # Clean up filename
            base_name = base_name.replace('#', '').replace('as Q60D', '').strip()
            output_path = os.path.join(enhanced_dir, f"{base_name}.mp4")
            
            # Convert with high quality settings
            cmd = f'ffmpeg -i "{video_path}" -c:v libx264 -crf 15 -preset slow -c:a aac -b:a 256k "{output_path}"'
            returncode, _, _ = self.run_command(cmd, show_output=True)
            
            if returncode == 0:
                self.print_success(f"Converted to: {base_name}.mp4")
                
                # Fix permissions on the new MP4
                self.run_command(f"chmod 777 '{output_path}'")
                
                if self.yes_no_prompt(f"Delete original {video_filename}?"):
                    os.remove(video_path)
                    self.print_success(f"Deleted {video_filename}")
            else:
                self.print_error(f"Failed to convert {video_filename}")
    
    def eject_cd(self):
        """Eject the CD"""
        self.print_info("Ejecting CD...")
        self.run_command(f"eject {self.cd_device}")
        self.print_success("CD ejected")
    
    def run(self):
        """Main workflow"""
        self.print_header("CD Ripper - Audio & Enhanced Content")
        
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Check for CD
        if not self.check_cd_inserted():
            return
        
        # Get CD info
        sessions = self.get_cd_info()
        
        # Ask to proceed
        if not self.yes_no_prompt("\nWould you like to proceed with ripping this CD?"):
            self.print_info("Operation cancelled")
            return
        
        # Rip audio
        if not self.rip_audio():
            self.print_error("Failed to rip audio tracks")
            return
        
        # Check for enhanced content
        if sessions > 1:
            self.print_info(f"\nThis appears to be an enhanced CD ({sessions} sessions)")
            if self.yes_no_prompt("Would you like to extract enhanced content (videos, images, etc.)?"):
                self.extract_enhanced_content()
        else:
            self.print_info("\nThis is a standard audio CD (1 session)")
            if self.yes_no_prompt("Would you still like to check for additional data content?"):
                self.extract_enhanced_content()
        
        # Eject
        if self.yes_no_prompt("\nWould you like to eject the CD?"):
            self.eject_cd()
        
        self.print_header("Ripping Complete!")
        self.print_success("All operations completed successfully")
        
        if self.yes_no_prompt("\nWould you like to rip another CD?"):
            print("\n" * 2)
            self.run()

def main():
    """Entry point"""
    try:
        ripper = CDRipper()
        ripper.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
