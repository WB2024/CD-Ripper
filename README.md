# [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?logo=buy-me-a-coffee)](https://buymeacoffee.com/succinctrecords)

# CD & DVD Ripper Suite

A comprehensive media ripping toolkit containing:
- **CD Ripper** - Extract audio CDs to FLAC with metadata and enhanced content support
- **DVD Ripper** - Extract music DVDs with configurable output formats (MP4, MKV, HEVC, audio-only)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

---

# CD Ripper - Audio & Enhanced Content

A comprehensive, interactive CD ripping tool that extracts audio tracks to FLAC format and handles enhanced CD content (videos, images, extras) with automatic metadata lookup and quality verification.

## Features

### Audio Ripping
- 🎵 **FLAC Output** - Maximum quality lossless compression (level 8)
- 🔍 **Automatic Metadata** - Fetches track info from CDDB/MusicBrainz
- ✏️ **Manual Entry** - Edit metadata during ripping process
- 📁 **Organized Output** - `Artist/Album/Track` folder structure
- 🔧 **Error Correction** - Uses cdparanoia with extensive retry logic
- ⚡ **Multi-core Encoding** - Parallel processing for faster rips

### Enhanced CD Support
- 💿 **Multi-session Detection** - Automatically identifies enhanced CDs
- 🎬 **Video Extraction** - Pulls music videos and extras
- 🖼️ **Image/Document Extraction** - Saves all bonus content
- 🔄 **Auto Conversion** - Converts FLV/MOV videos to MP4
- 📦 **Quality Preservation** - High-quality video transcoding

### User Experience
- 🎨 **Beautiful Interface** - Color-coded, easy-to-read output
- ✅ **Interactive Prompts** - Full control over each step
- 📊 **Progress Tracking** - See what's happening in real-time
- 🔁 **Batch Processing** - Rip multiple CDs in one session
- 🔐 **Permission Management** - Automatic 777 permissions for network shares

## Requirements

- **Operating System:** Linux (Debian/Ubuntu recommended)
- **Python:** 3.6 or higher
- **CD Drive:** Any standard CD/DVD drive
- **Root/sudo access:** For installation and CD drive access

### Required Packages
- `abcde` - A Better CD Encoder
- `cdparanoia` - CD reading with error correction
- `flac` - FLAC encoder
- `ffmpeg` - Video/audio processing
- `cdrdao` - CD information and TOC reading

## Installation

### Quick Install (Recommended)

```bash
# Download the script
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/cd-ripper.py

# Download the configuration file
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/.abcde.conf

# Make script executable
chmod +x cd-ripper.py

# Move script to system bin
sudo mv cd-ripper.py /usr/local/bin/

# Move config to home directory
mv .abcde.conf ~/.abcde.conf

# Create convenient alias (optional)
sudo ln -s /usr/local/bin/cd-ripper.py /usr/local/bin/cd-ripper
```

The script will automatically offer to install missing dependencies on first run.

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WB2024/CD-Ripper.git
   cd CD-Ripper
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install abcde cdparanoia flac ffmpeg cdrdao python3
   ```

3. **Install the script:**
   ```bash
   chmod +x cd-ripper.py
   sudo cp cd-ripper.py /usr/local/bin/
   cp .abcde.conf ~/.abcde.conf
   sudo ln -s /usr/local/bin/cd-ripper.py /usr/local/bin/cd-ripper
   ```

4. **Verify installation:**
   ```bash
   cd-ripper
   ```

## Configuration

### abcde Configuration

The included `.abcde.conf` file is pre-configured with optimal settings:

```bash
# Output format
OUTPUTTYPE="flac"
FLACOPTS='-s -e -V -8'  # Maximum compression

# CD ripper
CDROMREADERSYNTAX=cdparanoia
CDPARANOIAOPTS="--never-skip=40"  # Extensive error correction

# Metadata
CDDBMETHOD=cddb  # Uses CDDB for lookups
INTERACTIVE=y     # Allows manual editing

# Output directory
OUTPUTDIR="/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/CD Rips"

# File structure
OUTPUTFORMAT='${ARTISTFILE}/${ALBUMFILE}/${TRACKNUM} - ${TRACKFILE}'
```

**Customize the output directory:**

Edit `~/.abcde.conf` and change the `OUTPUTDIR` line:

```bash
nano ~/.abcde.conf
# Change OUTPUTDIR to your preferred location
# Example: OUTPUTDIR="/home/youruser/Music/CD Rips"
```

### CD Drive Configuration

By default, the script uses `/dev/sr0`. If your drive is different:

Edit the script:
```bash
sudo nano /usr/local/bin/cd-ripper.py
```

Find and change:
```python
self.cd_device = "/dev/sr0"  # Change to your device
```

**Find your CD drive:**
```bash
lsblk
# Look for sr0, sr1, etc.
```

## Usage

### Basic Workflow

1. **Insert CD** into your drive

2. **Run the script:**
   ```bash
   cd-ripper
   ```

3. **Follow the interactive prompts:**
   - ✓ Dependency check (auto-install if needed)
   - ✓ CD detection
   - ✓ Track analysis
   - ✓ Proceed with rip? (y/n)
   - ✓ Edit metadata (artist, album, tracks)
   - ✓ Audio ripping with progress
   - ✓ Check for enhanced content? (y/n)
   - ✓ Extract videos/extras (if found)
   - ✓ Convert videos to MP4? (y/n)
   - ✓ Eject CD? (y/n)
   - ✓ Rip another CD? (y/n)

### Example Session

```
============================================================
            CD Ripper - Audio & Enhanced Content
============================================================

Checking Dependencies
✓ abcde is installed
✓ cdparanoia is installed
✓ flac is installed
✓ ffmpeg is installed
✓ cdrdao is installed

Checking for CD
✓ CD detected!

Analyzing CD
ℹ Sessions found: 2

Table of contents (audio tracks only):
track        length               begin        copy pre ch
===========================================================
  1.    14205 [03:09.30]        0 [00:00.00]    no   no  2
  2.    27697 [06:09.22]    14205 [03:09.30]    no   no  2
  3.    17008 [03:46.58]    41902 [09:18.52]    no   no  2
TOTAL   58910 [13:05.35]    (audio only)

Would you like to proceed with ripping this CD? (y/n): y

[Metadata lookup and editing...]
[Audio ripping with progress...]

✓ Audio ripping completed!
ℹ Setting permissions for: /path/to/output
✓ Permissions set successfully (777)

ℹ This appears to be an enhanced CD (2 sessions)
Would you like to extract enhanced content (videos, images, etc.)? (y/n): y

[Enhanced content extraction...]
✓ Enhanced content saved to: /path/to/output/Enhanced Content

Found 2 video file(s)
  - clip.flv
  - music_video.mov

Would you like to convert these videos to MP4? (y/n): y

[Video conversion with progress...]
��� Converted to: clip.mp4
✓ Converted to: music_video.mp4

Would you like to eject the CD? (y/n): y
✓ CD ejected

============================================================
                    Ripping Complete!
============================================================
✓ All operations completed successfully

Would you like to rip another CD? (y/n): n
```

## Output Structure

### Standard CD

```
CD Rips/
└── Artist Name/
    └── Album Name/
        ├── 01 - Track One.flac
        ├── 02 - Track Two.flac
        ├── 03 - Track Three.flac
        └── ...
```

### Enhanced CD

```
CD Rips/
└── Artist Name/
    └── Album Name/
        ├── 01 - Track One.flac
        ├── 02 - Track Two.flac
        ├── 03 - Track Three.flac
        └── Enhanced Content/
            ├── music_video.mp4
            ├── behind_the_scenes.mp4
            ├── photos/
            └── liner_notes.pdf
```

## Features Deep Dive

### Audio Quality

**CD Audio Specifications:**
- Sample Rate: 44.1 kHz (44,100 Hz)
- Bit Depth: 16-bit
- Channels: 2 (stereo)
- Bitrate (uncompressed): 1,411 kbps

**FLAC Compression:**
- Level 8 (maximum compression)
- Lossless (bit-perfect audio)
- Typically 40-60% smaller than WAV
- Full metadata support

**Error Correction:**
- cdparanoia with `--never-skip=40`
- Re-reads errors up to 40 times
- Interpolates unreadable sectors
- Verifies read quality

### Enhanced CD Support

**What are Enhanced CDs?**
Enhanced CDs (CD-Plus, CD-Extra) contain:
- Session 1: Standard audio tracks
- Session 2: Data files (videos, images, software)

**Supported Content Types:**
- Videos: .mov, .flv, .avi, .mpg
- Images: .jpg, .png, .bmp
- Documents: .pdf, .txt
- Software: .exe (preserved but not executed)

**Video Conversion:**
- Source formats: FLV, MOV, AVI, WMV, MPG
- Output: MP4 (H.264/AAC)
- Quality: CRF 15 (near-lossless)
- Preset: Slow (better compression)
- Audio: AAC 256kbps

### Metadata Handling

**Automatic Lookup:**
1. Calculates disc ID from TOC
2. Queries CDDB database
3. If not found, prompts for manual entry

**Editable Fields:**
- Artist name
- Album title
- Album year
- Genre
- Track titles
- Track artists (for compilations)

**Disc ID:**
The disc ID is unique to each CD pressing and calculated from:
- Number of tracks
- Track start positions
- Total disc length

### Permission Management

All output files and directories are automatically set to 777 permissions:
- Useful for network shares (SMB/NFS)
- Allows full access from any user
- Can be disabled if not needed

## Troubleshooting

### "No CD detected"

**Causes:**
- CD not inserted
- Drive not ready
- Wrong device path

**Solutions:**
```bash
# Check if drive exists
ls -l /dev/sr*

# Check if CD is mounted
mount | grep sr0

# Unmount if necessary
sudo umount /dev/sr0

# Try ejecting and reinserting
eject
```

### "abcde: abcde-musicbrainz-tool failed"

**Cause:** MusicBrainz lookup failure (network/API issue)

**Solution:** The script uses CDDB as primary source. If both fail:
- Manual metadata entry will be prompted
- Or edit `~/.abcde.conf` and set:
  ```bash
  CDDBMETHOD=cdtext  # Skip online lookup
  ```

### "Failed to mount enhanced content"

**Causes:**
- Not an enhanced CD (only 1 session)
- Data session is damaged
- Permissions issue

**Solutions:**
```bash
# Check sessions manually
cdrdao disk-info --device /dev/sr0

# Try manual mount
sudo mount -t iso9660 -o session=1,ro /dev/sr0 /mnt/test
ls /mnt/test
sudo umount /mnt/test
```

### Scratched/Damaged CDs

cdparanoia will:
- Re-read errors multiple times
- Report problematic sectors
- Interpolate if necessary

**Check for errors:**
```bash
# Watch output during ripping for lines like:
# "Skipped sector corrected"
# "Unreported error corrected"
```

If too many errors, the CD may be too damaged.

### Permission Denied Errors

**Solution:**
```bash
# Run with sudo (CD drive access requires root)
sudo cd-ripper

# Or add user to cdrom group
sudo usermod -a -G cdrom $USER
# Log out and back in
```

## Advanced Usage

### Batch Ripping

The script supports continuous ripping:

1. Rip first CD
2. When asked "Rip another CD?", choose Yes
3. Eject current CD
4. Insert next CD
5. Repeat

### Custom Output Directory

**Temporary change:**
```bash
# Edit config for this session
nano ~/.abcde.conf
# Change OUTPUTDIR, save, and run cd-ripper
```

**Permanent change:**
Update the `OUTPUTDIR` in `~/.abcde.conf`

### Skip Enhanced Content

Just answer "No" when prompted:
```
Would you like to extract enhanced content? (y/n): n
```

### Network Storage

The tool works great with network shares:

```bash
# Mount network share
sudo mount -t cifs //server/music /mnt/music -o username=user

# Update output directory
nano ~/.abcde.conf
# Set: OUTPUTDIR="/mnt/music/CD Rips"

# Run ripper
cd-ripper
```

The 777 permissions ensure files are accessible from other devices.

## Technical Details

### Dependencies Explained

| Package | Purpose |
|---------|---------|
| `abcde` | Orchestrates the ripping workflow |
| `cdparanoia` | Reads audio from CD with error correction |
| `flac` | Encodes audio to FLAC format |
| `ffmpeg` | Converts enhanced content videos |
| `cdrdao` | Reads CD Table of Contents and session info |
| `python3` | Runs the main script |

### File Naming

**Sanitization:**
- Removes invalid characters: `/ \ : * ? " < > |`
- Replaces spaces with spaces (configurable)
- Handles special characters in Unicode

**Format:**
```
Artist/Album/##  - Track Title.flac
```

Example:
```
Morrissey/You Have Killed Me/01 - You Have Killed Me.flac
```

### Disc Reading Process

1. **Detection** - Check if CD is present
2. **TOC Reading** - Get track positions and count
3. **Disc ID Calculation** - Generate unique identifier
4. **Metadata Lookup** - Query CDDB/MusicBrainz
5. **Ripping** - Read audio with error correction
6. **Encoding** - Convert to FLAC
7. **Tagging** - Add metadata
8. **Organization** - Move to proper folder structure

## FAQ

**Q: Will this work with copy-protected CDs?**  
A: Most copy protection schemes from the early 2000s can be read by cdparanoia. Modern CDs rarely have protection.

**Q: How long does it take to rip a CD?**  
A: Typically 5-15 minutes depending on:
- CD length
- Drive speed
- Number of errors
- System performance

**Q: Can I rip DVDs or Blu-rays?**  
A: Yes! Use the included `dvd-ripper.py` for music DVDs. For Blu-rays, use HandBrake or MakeMKV directly.

**Q: What's the difference between CDDB and MusicBrainz?**  
A: Both are metadata databases. CDDB (now Gracenote) is older and more reliable. MusicBrainz is open-source but sometimes has API issues.

**Q: Will ripping damage my CDs?**  
A: No, reading data from a CD does not damage it.

**Q: Can I edit metadata after ripping?**  
A: Yes, use tools like:
- `metaflac` (command-line)
- MusicBrainz Picard (GUI)
- Any music player with tagging support

**Q: Are the rips bit-perfect?**  
A: Yes, with proper error correction, FLAC rips are bit-for-bit identical to the CD.

**Q: What if my album isn't in the CDDB?**  
A: You'll be prompted to enter metadata manually during the ripping process.

## Use Cases

### Archive CD Collection
```bash
# Perfect for digitizing your entire music library
# Lossless quality ensures perfect preservation
cd-ripper
```

### Backup Rare CDs
```bash
# Create digital backups of out-of-print albums
# Enhanced content preserved for completeness
cd-ripper
```

### Prepare for Music Server
```bash
# Rip CDs for Plex, Jellyfin, Navidrome, etc.
# FLAC is supported by all modern servers
cd-ripper
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional metadata sources
- DVD-Audio support
- AccurateRip verification
- Batch processing improvements

```bash
git clone https://github.com/WB2024/CD-Ripper.git
cd CD-Ripper
# Make changes
# Submit pull request
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

**WB2024**
- GitHub: [@WB2024](https://github.com/WB2024)

## Acknowledgments

- [abcde](https://abcde.einval.com/) - A Better CD Encoder
- [cdparanoia](https://www.xiph.org/paranoia/) - Paranoia CD reading
- [FLAC](https://xiph.org/flac/) - Free Lossless Audio Codec
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework
- [CDDB/Gracenote](https://www.gracenote.com/) - Metadata provider

## Related Projects

- **[Audio to FLAC Converter](https://github.com/WB2024/Convert-Audio-to-FLAC)** - Convert any audio format to FLAC
- **[MusicBrainz Picard](https://picard.musicbrainz.org/)** - Music tagger
- **[Exact Audio Copy](http://www.exactaudiocopy.de/)** - Windows alternative

## Changelog

### v1.0.0 (2025-02-17)
- Initial release
- FLAC audio ripping with CDDB metadata
- Enhanced CD support (multi-session)
- Video extraction and MP4 conversion
- Interactive workflow
- Automatic permission management
- Batch processing support

---

# DVD Ripper - Music DVD Edition

A companion tool for extracting and converting music DVD content with configurable output formats. Uses **HandBrake CLI** (GPLv2, free forever) for extraction and conversion.

## Why HandBrake?

- **Free Forever** - GPLv2 open-source license, will never become paid software
- **All-in-One** - Handles DVD decryption, extraction, and encoding in a single tool
- **Actively Maintained** - Regular updates, large community, excellent documentation
- **Built-in Presets** - Optimized quality settings out of the box
- **libdvdcss Integration** - Handles encrypted DVDs when libdvdcss is installed

## DVD Ripper Features

### Video Extraction
- 📀 **HandBrake Backend** - Free, open-source DVD handling
- 🔓 **DVD Decryption** - Works with libdvdcss for encrypted DVDs
- 🎬 **Multiple Formats** - MP4, MKV, HEVC output options
- ⚙️ **Quality Presets** - High, Balanced, Fast encoding
- 🎵 **Audio Extraction** - FLAC/MP3 audio-only mode

### Output Formats

| Format | Encoder | Best For |
|--------|---------|----------|
| MP4 (H.264) | x264 | Maximum compatibility |
| MKV (H.264) | x264 | Multiple audio/subtitle tracks |
| MP4 (H.265) | x265 | Smaller files, modern devices |
| FLAC | flac | Lossless audio extraction |
| MP3 | lame | Compressed audio |

### Quality Presets

| Preset | Quality (RF) | Speed | File Size |
|--------|--------------|-------|-----------|
| High Quality | 18 | Slow | Larger |
| Balanced | 22 | Medium | Moderate |
| Fast/Smaller | 26 | Fast | Smaller |

## DVD Ripper Requirements

### Required Packages
- `handbrake-cli` - HandBrake command-line interface (GPLv2)
- `libdvd-pkg` - Downloads and installs libdvdcss for DVD decryption
- `lsdvd` - DVD information tool
- `ffmpeg` - Video/audio processing (for audio extraction)

## DVD Ripper Installation

### Debian/Ubuntu/OpenMediaVault (All Versions)

```bash
# Update package list
sudo apt update

# Install HandBrake CLI, FFmpeg, and lsdvd
sudo apt install handbrake-cli ffmpeg lsdvd

# Install libdvdcss for encrypted DVD support
sudo apt install libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

# Download DVD ripper script
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/dvd-ripper.py
chmod +x dvd-ripper.py
sudo cp dvd-ripper.py /usr/local/bin/
sudo ln -sf /usr/local/bin/dvd-ripper.py /usr/local/bin/dvd-ripper

# Verify installation
HandBrakeCLI --version
```

### Ubuntu/Linux Mint (PPA for latest version)

```bash
# Add HandBrake PPA for latest version (optional)
sudo add-apt-repository ppa:stebbins/handbrake-releases
sudo apt update

# Install packages
sudo apt install handbrake-cli ffmpeg lsdvd libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

# Download DVD ripper script
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/dvd-ripper.py
chmod +x dvd-ripper.py
sudo mv dvd-ripper.py /usr/local/bin/
sudo ln -sf /usr/local/bin/dvd-ripper.py /usr/local/bin/dvd-ripper
```

### Arch Linux

```bash
# Install from official repos
sudo pacman -S handbrake-cli ffmpeg lsdvd libdvdcss

# Download DVD ripper script
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/dvd-ripper.py
chmod +x dvd-ripper.py
sudo mv dvd-ripper.py /usr/local/bin/
sudo ln -sf /usr/local/bin/dvd-ripper.py /usr/local/bin/dvd-ripper
```

### Fedora/RHEL/CentOS

```bash
# Enable RPM Fusion repository (for ffmpeg and libdvdcss)
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

# Install HandBrake CLI and dependencies
sudo dnf install HandBrake-cli ffmpeg lsdvd libdvdcss

# Download DVD ripper script
curl -O https://raw.githubusercontent.com/WB2024/CD-Ripper/main/dvd-ripper.py
chmod +x dvd-ripper.py
sudo mv dvd-ripper.py /usr/local/bin/
sudo ln -sf /usr/local/bin/dvd-ripper.py /usr/local/bin/dvd-ripper
```

### Other Distributions

HandBrake is available for most Linux distributions:
- **Flatpak:** `flatpak install flathub fr.handbrake.ghb`
- **Snap:** `snap install handbrake-jz` (includes CLI)
- **From source:** [https://handbrake.fr/downloads.php](https://handbrake.fr/downloads.php)

Don't forget to also install `libdvdcss` for encrypted DVD support.

## DVD Ripper Usage

### Basic Workflow

```bash
dvd-ripper
```

1. **Insert DVD** into your drive
2. **Select output format** - MP4, MKV, HEVC, or Audio-only
3. **Select quality preset** - High, Balanced, or Fast
4. **Enter metadata** - Artist name, album/DVD title
5. **Choose ripping mode**:
   - Batch Mode: Process all titles automatically
   - Selective Mode: Choose specific titles to rip
6. **Wait for extraction and conversion**
7. **Eject DVD** when complete

### Example Session

```
╔═══════════════════════════════════════════════════════════╗
║              DVD Ripper - Music DVD Edition               ║
║       Powered by HandBrake CLI (Free & Open Source)       ║
╚═══════════════════════════════════════════════════════════╝

============================================================
                   Checking Dependencies
============================================================

✓ HandBrake CLI is installed
✓ FFmpeg is installed
✓ FFprobe is installed
✓ lsdvd is installed
✓ libdvdcss is installed (DVD decryption)

============================================================
                     Checking for DVD
============================================================

✓ DVD detected!

============================================================
                      Analyzing DVD
============================================================

  Disc Title: MUSIC_CONCERT_2024
  Titles found: 12

============================================================
                   Select Output Format
============================================================

  1. MP4 (H.264)
     Most compatible - works on all devices
  2. MKV (H.264)
     Best for multiple audio/subtitle tracks
  3. MP4 (H.265/HEVC)
     Smaller files, modern devices only
  4. Audio Only (FLAC)
     Lossless audio extraction
  5. Audio Only (MP3)
     Compressed audio extraction

Select option (1-5): 1
✓ Selected: MP4 (H.264)

============================================================
                  Select Quality Preset
============================================================

  1. High Quality (Larger files)
     Best quality, larger file size
  2. Balanced (Recommended)
     Good quality with reasonable file size
  3. Fast/Smaller (Lower quality)
     Faster encoding, smaller files

Select option (1-3): 2
✓ Selected: Balanced (Recommended)

============================================================
                     Output Settings
============================================================

Enter Artist/Band name [Unknown Artist]: The Rolling Stones
Enter Album/DVD title [MUSIC_CONCERT_2024]: Live Concert 2024
✓ Output directory: /srv/.../DVD Rips/The Rolling Stones/Live Concert 2024

Would you like to proceed with ripping this DVD? (y/n): y

Select ripping mode:
  1. Batch Mode - Rip all titles automatically
  2. Selective Mode - Choose which titles to rip
Select mode (1/2): 1

[Extraction and conversion progress...]

============================================================
                     Ripping Summary
============================================================

Converted files:
  ✓ 01 - Track 01.mp4 (450.2 MB)
  ✓ 02 - Track 02.mp4 (380.1 MB)
  ✓ 03 - Track 03.mp4 (520.5 MB)

Total: 12 file(s), 5.2 GB
Location: /srv/.../DVD Rips/The Rolling Stones/Live Concert 2024

✓ Permissions set successfully (777)

Would you like to eject the DVD? (y/n): y
✓ DVD ejected

============================================================
                     Ripping Complete!
============================================================
✓ All operations completed successfully
```

## DVD Output Structure

```
DVD Rips/
└── Artist Name/
    └── Album or DVD Title/
        ├── 01 - Track 01.mp4
        ├── 02 - Track 02.mp4
        ├── 03 - Track 03.mp4
        └── ...
```

## DVD Ripper Configuration

### Customizing Output Location

**Method 1: Edit the script**

```bash
sudo nano /usr/local/bin/dvd-ripper.py
```

Find and change:
```python
self.base_output_dir = "/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/DVD Rips"
```

To your preferred location:
```python
self.base_output_dir = "/home/youruser/Videos/DVD Rips"
```

**Method 2: Create a symlink**

```bash
ln -s /your/actual/path "/srv/dev-disk-by-uuid-dc4918d5-6597-465b-9567-ce442fbd8e2a/DVD Rips"
```

### DVD Drive Configuration

If your DVD drive is not `/dev/sr0`:

```bash
# Find your DVD drive
lsblk
ls -l /dev/sr*

# Edit the script
sudo nano /usr/local/bin/dvd-ripper.py

# Change this line:
self.dvd_device = "/dev/sr0"  # Change to /dev/sr1, etc.
```

### Temp Directory

HandBrake encodes directly without an intermediate step, so no temporary directory is needed for most operations. Audio extraction uses a temporary MKV file in `/tmp`.

## Features Deep Dive

### Format Comparison

**MP4 (H.264)** - Universal Compatibility
- Codec: H.264/AVC with AAC audio
- Compatible with virtually all devices
- Good compression ratio
- Widely supported by media servers
- Best for: Sharing, streaming, maximum compatibility

**MKV (H.264)** - Feature-Rich Container
- Codec: H.264/AVC with FLAC or AAC audio
- Supports multiple audio tracks (e.g., commentary, different languages)
- Supports multiple subtitle tracks
- Supports chapters and metadata
- Best for: Archival, multiple audio/subtitle options

**MP4 (H.265/HEVC)** - Maximum Compression
- Codec: H.265/HEVC with AAC audio
- 30-50% smaller files than H.264 at same quality
- Requires modern devices (2015+)
- Slower encoding time
- Best for: Storage savings, modern device ecosystems

**Audio Only (FLAC)** - Lossless Audio
- No video, audio only
- Bit-perfect audio extraction
- Larger file sizes than MP3
- Best for: Music performances, concerts (audio focus)

**Audio Only (MP3)** - Compressed Audio
- No video, audio only
- Significantly smaller files
- Slight quality loss
- Best for: Portable audio, streaming

### Quality Settings Explained

**High Quality (CRF 18)**
- Near-transparent quality
- Recommended for archival purposes
- File size: ~2-4 GB per hour of video
- Encoding time: Slow (1-2x realtime on modern CPU)

**Balanced (CRF 22)** - RECOMMENDED
- Excellent quality, most people can't see difference
- Great balance of quality and file size
- File size: ~1-2 GB per hour of video
- Encoding time: Medium (2-4x realtime)

**Fast/Smaller (CRF 26)**
- Good quality, some artifacts visible on close inspection
- Smaller files for portable devices
- File size: ~0.5-1 GB per hour of video
- Encoding time: Fast (4-6x realtime)

**CRF Explained:**
- Constant Rate Factor (CRF) controls video quality
- Lower CRF = higher quality, larger files
- Range: 0 (lossless) to 51 (worst quality)
- CRF 18-22 considered "visually lossless"

### The Ripping Process

1. **DVD Detection** - Checks if DVD is inserted and readable
2. **Disc Analysis** - Scans DVD structure with lsdvd and HandBrake
3. **Format Selection** - User chooses output format and quality
4. **Metadata Entry** - User provides artist/album information
5. **HandBrake Extraction & Encoding** - Single-pass decryption, extraction, and encoding
6. **Organization** - Saves files to artist/album folder structure
7. **Cleanup** - Sets permissions for network share access

### Why HandBrake?

**Advantages of HandBrake for DVD ripping:**

- **Free Forever:** GPLv2 license - will never become paid software
- **All-in-One:** Decryption + extraction + encoding in a single pass
- **libdvdcss Integration:** Handles CSS encryption when libdvdcss is installed
- **Optimized Presets:** Built-in quality settings tested by experts
- **Active Development:** Regular updates and large community support
- **No Registration:** Unlike some alternatives, no keys or licenses required

## DVD Types Supported

### Music DVDs
- Concert performances
- Live albums
- Music video collections
- Behind-the-scenes documentaries
- Special editions with bonus content

### Commercial Music Video DVDs
- Artist video compilations
- MTV/VH1 collections
- Themed video collections

### Video Quality Expectations

**DVD Video Specifications:**
- Resolution: 720×480 (NTSC) or 720×576 (PAL)
- Aspect Ratio: Usually 16:9 or 4:3
- Bitrate: ~5-8 Mbps average
- Audio: AC3, DTS, PCM, or MP2

**Output Quality:**
- Maintained at source resolution (no upscaling)
- Deinterlaced when necessary
- Color space preserved
- Audio transcoded to selected format

## Advanced Usage

### Batch Processing Multiple DVDs

The script supports continuous ripping:

```bash
dvd-ripper
# Rip first DVD, then when asked "Rip another DVD?" choose Yes
# Eject, insert next DVD, repeat
```

### Selective Title Ripping

Use Selective Mode when DVDs have both main content and extras:

1. Choose **Selective Mode** when prompted
2. HandBrake will scan all titles
3. Review list with file sizes and durations
4. Enter which titles to convert (e.g., `1,3,5` or `all`)
5. Name each title individually

**Example:**
```
Extracted titles:
  1. title00.mkv (4.2 GB, 45m 30s)  ← Main concert
  2. title01.mkv (150 MB, 2m 45s)   ← Trailer
  3. title02.mkv (800 MB, 12m 15s)  ← Behind the scenes

Enter title numbers to convert: 1,3
```

### Network Storage

Works great with NAS/network shares:

```bash
# Mount network share
sudo mount -t cifs //nas/videos /mnt/nas -o username=user,password=pass

# Update output directory in script or create symlink
sudo ln -s /mnt/nas "/srv/long-path/DVD Rips"

# Run ripper - 777 permissions ensure NAS compatibility
dvd-ripper
```

### Custom FFmpeg Arguments

For advanced users wanting custom encoding:

Edit [dvd-ripper.py](dvd-ripper.py) in the `convert_file()` method to add custom FFmpeg flags.

Example additions:
```python
# Add 2-pass encoding
# Add custom filters
# Add HDR metadata
# Add specific audio tracks
```

## DVD Ripper Troubleshooting

### "HandBrake CLI not found"

**Install on Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install handbrake-cli
```

**Other distributions:**
- **Fedora:** `sudo dnf install HandBrake-cli`
- **Arch:** `sudo pacman -S handbrake-cli`
- **Flatpak:** `flatpak install flathub fr.handbrake.ghb`

**Verify installation:**
```bash
which HandBrakeCLI
HandBrakeCLI --version
```

### "No DVD detected"

**Check drive exists:**
```bash
ls -l /dev/sr*
# Should show: /dev/sr0, /dev/sr1, etc.
```

**Test with lsdvd:**
```bash
lsdvd /dev/sr0
# Should show DVD information
```

**If DVD is mounted (prevents ripping):**
```bash
mount | grep sr0
sudo umount /dev/sr0
```

**Drive not spinning up:**
- Ensure DVD is fully inserted
- Try ejecting and reinserting
- Check drive with: `sudo hdparm -I /dev/sr0`

### "HandBrake extraction failed" / Encrypted DVD Issues

**Install libdvdcss for DVD decryption:**
```bash
# Debian/Ubuntu
sudo apt install libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

# Fedora (RPM Fusion required)
sudo dnf install libdvdcss

# Arch
sudo pacman -S libdvdcss
```

**Test manually:**
```bash
# Scan DVD with HandBrake
HandBrakeCLI --input /dev/sr0 --title 0 --scan

# Try ripping title 1 to test
HandBrakeCLI --input /dev/sr0 --title 1 --output test.mp4
```

**Common causes:**
- Damaged/dirty disc - clean with microfiber cloth
- libdvdcss not installed - required for encrypted DVDs
- Read error - try in different drive

### "FFmpeg conversion failed" (Audio extraction)

**Check FFmpeg codecs:**
```bash
ffmpeg -codecs | grep -E 'h264|h265|hevc'
ffmpeg -encoders | grep -E 'libx264|libx265'
```

**If libx264 missing:**
```bash
sudo apt install ffmpeg libavcodec-extra
```

**If libx265 missing:**
```bash
sudo apt install libx265-dev
```

**Test manual conversion:**
```bash
ffmpeg -i /tmp/dvd-ripper/title00.mkv -c:v libx264 -crf 22 test.mp4
```

### Encrypted/Protected DVDs

**CSS Encryption:**
HandBrake uses libdvdcss when available. Install it:
```bash
# Debian/Ubuntu
sudo apt install libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

# Fedora (RPM Fusion)
sudo dnf install libdvdcss

# Arch
sudo pacman -S libdvdcss
```

**Region Codes:**
- HandBrake with libdvdcss bypasses region locks
- No drive firmware modification needed

**ARccOS, RipGuard, etc.:**
- libdvdcss handles CSS encryption (most common)
- More advanced protections may not be supported
- This is a limitation of free/open-source tools

**If still failing:**
- Ensure libdvdcss is correctly installed
- Try another drive (different chipset)
- Verify disc plays in regular DVD player
- Some newer protections may require alternative tools

### "Out of space" errors

**Output directory full:**
```bash
# Check space
df -h /path/to/DVD\ Rips
```

**General guidance:**
- DVD source: ~4-8 GB per disc
- Final output: 1-4 GB (depending on format/quality)
- Total space needed: ~5-10 GB free during ripping

### Permission issues

**Run with sudo:**
```bash
sudo dvd-ripper
```

**Or add user to cdrom group:**
```bash
sudo usermod -a -G cdrom $USER
# Log out and back in for changes to take effect
```

**Output directory permissions:**
```bash
sudo chmod -R 777 "/path/to/DVD Rips"
# Or better, set ownership:
sudo chown -R $USER:$USER "/path/to/DVD Rips"
```

### Slow ripping/encoding

**Extraction slow:**
- DVD drive speed limitation (usually 8-16x)
- Damaged disc requires multiple retries
- Normal: 10-30 minutes for extraction

**Encoding slow:**
- CPU-intensive process
- HEVC (H.265) is slower than H.264
- "High Quality" preset is slower than "Fast"
- Normal speeds:
  - H.264 Fast: 4-6x realtime
  - H.264 Medium: 2-4x realtime
  - H.264 Slow: 1-2x realtime
  - H.265: 50% slower than H.264

**Speed improvements:**
```bash
# Use faster preset (in script)
preset = 'fast'  # instead of 'medium' or 'slow'

# Use H.264 instead of H.265

# Lower CRF (lower quality, faster)
crf = 26  # instead of 18 or 22
```

## DVD Ripper FAQ

**Q: Will this work with commercial DVDs?**  
A: Yes, HandBrake with libdvdcss handles encrypted/protected commercial music DVDs.

**Q: Can I rip multi-disc DVD sets?**  
A: Yes, rip each disc separately. The script supports continuous processing.

**Q: How long does it take to rip a DVD?**  
A: Typically 30-60 minutes total:
- Extraction: 10-30 minutes (depends on drive speed)
- Conversion: 20-45 minutes (depends on format, quality, CPU)

**Q: Will this work with Blu-rays?**  
A: Not directly with this script. For Blu-rays, use HandBrake GUI or MakeMKV (free during beta). This script is optimized for DVDs.

**Q: Can I preserve multiple audio tracks?**  
A: Yes, use MKV format. FFmpeg will preserve all audio tracks by default.

**Q: What about subtitles?**  
A: MKV format preserves all subtitles. MP4 may lose some subtitle tracks.

**Q: How do I add chapters?**  
A: MKV format preserves DVD chapters automatically.

**Q: Can I upscale DVD to 1080p?**  
A: Not recommended. DVD is 480p/576p max. Upscaling doesn't add detail, just makes files larger. Better to keep source resolution.

**Q: Which format should I choose?**  
A: 
- **General use:** MP4 (H.264) - works everywhere
- **Archival:** MKV (H.264) - preserves all features
- **Storage limited:** MP4 (H.265) - smallest files
- **Audio only:** FLAC - perfect for concerts where video isn't important

**Q: Are the rips as good as the original DVD?**  
A: With High Quality preset (CRF 18), visually identical. With Balanced (CRF 22), most people cannot see any difference.

**Q: Can I edit metadata after ripping?**  
A: Yes, use tools like:
- `ffmpeg` - Command-line metadata editing
- MKVToolNix - GUI for MKV files
- MediaInfo - View metadata
- VLC, Kodi, Plex - Edit metadata in media library

**Q: What if the DVD has multiple camera angles?**  
A: HandBrake extracts the default angle. Multiple angles may create separate tracks.

**Q: Can I rip copy-protected DVDs legally?**  
A: Laws vary by country. In many regions, personal backups are legal. Check local laws.

## Use Cases

### Archive Concert DVD Collection
```bash
# Preserve your concert DVDs digitally
# MKV format maintains all features
# High Quality preset for archival
dvd-ripper
# Select: MKV (H.264), High Quality
```

### Convert for Mobile Devices
```bash
# Smaller files for phones/tablets
dvd-ripper
# Select: MP4 (H.265), Fast/Smaller
```

### Extract Audio from Concert DVDs
```bash
# Get just the audio for music library
dvd-ripper
# Select: Audio Only (FLAC)
# Import to Plex, Jellyfin, etc.
```

### Prepare for Media Server
```bash
# Rip entire collection for Plex/Jellyfin
# MP4 for maximum compatibility
dvd-ripper
# Select: MP4 (H.264), Balanced
```

## Technical Details

### Dependencies Explained

| Package | Purpose |
|---------|---------|
| `handbrake-cli` | DVD ripping, encoding, and format conversion (GPLv2) |
| `libdvdcss` | CSS decryption for encrypted DVDs (via libdvd-pkg) |
| `lsdvd` | Reads DVD structure and title information |
| `ffmpeg` | Audio extraction and additional processing |
| `ffprobe` | Analyzes video metadata and duration |
| `python3` | Runs the main script |

### File Naming

**Sanitization:**
- Removes invalid characters: `/ \ : * ? " < > |`
- Replaces underscores with spaces
- Handles Unicode characters

**Format:**
```
Artist/Album/## - Track Name.ext
```

**Example:**
```
The Rolling Stones/Live Concert 2024/01 - Track 01.mp4
```

### Encoding Details (HandBrake)

**H.264 Settings:**
```
--encoder x264
--quality 18-26     (RF/CRF - lower = better)
--encoder-preset slow/medium/fast
--aencoder av_aac
--ab 256
```

**H.265/HEVC Settings:**
```
--encoder x265
--quality 18-26
--encoder-preset slow/medium/fast
--aencoder av_aac
--ab 256
```

**Audio Extraction (via FFmpeg):**
```bash
# FLAC (lossless)
ffmpeg -i input.mkv -vn -acodec flac output.flac

# MP3 (320kbps)
ffmpeg -i input.mkv -vn -acodec libmp3lame -ab 320k output.mp3
```

## Comparison: CD Ripper vs DVD Ripper

| Feature | CD Ripper | DVD Ripper |
|---------|-----------|------------|
| **Primary Use** | Audio CDs | Music DVDs |
| **Backend** | abcde + cdparanoia | HandBrake CLI (GPLv2) |
| **Output Formats** | FLAC only | MP4, MKV, HEVC, FLAC, MP3 |
| **Quality Control** | Fixed (lossless) | Configurable (RF 18-26) |
| **Metadata** | CDDB/MusicBrainz | Manual entry |
| **Enhanced Content** | Yes (2nd session) | N/A |
| **Encryption Handling** | N/A (CDs not encrypted) | Yes (libdvdcss) |
| **Batch Processing** | Yes | Yes |
| **Selective Ripping** | No (all tracks) | Yes (choose titles) |
| **License** | GPL (free) | GPL (free forever) |

## Related Tools & Resources

### Complementary Software
- **HandBrake GUI** - Visual interface for HandBrake
- **VLC** - Media player with DVD ripping capability
- **VidCoder** - Windows HandBrake fork
- **MakeMKV** - Alternative (free during beta, paid after)

### Media Servers
- **Plex** - Popular media server
- **Jellyfin** - Open-source Plex alternative
- **Emby** - Media server platform
- **Kodi** - Media center software

### Metadata Tools
- **MKVToolNix** - Edit MKV metadata
- **MediaInfo** - View media file information
- **tinyMediaManager** - Organize and tag video library

### Useful Resources
- [HandBrake Documentation](https://handbrake.fr/docs/) - Official guides and best practices
- [HandBrake Community](https://forum.handbrake.fr/) - Support and community help
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) - Encoding guides
- [CRF Guide](https://trac.ffmpeg.org/wiki/Encode/H.264) - Understanding CRF/RF values
- [VideoHelp DVD Forum](https://forum.videohelp.com/forums/2-DVD) - DVD ripping discussion

---

**Happy Ripping! 💿📀**
