# [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?logo=buy-me-a-coffee)](https://buymeacoffee.com/succinctrecords)

# CD Ripper - Audio & Enhanced Content

A comprehensive, interactive CD ripping tool that extracts audio tracks to FLAC format and handles enhanced CD content (videos, images, extras) with automatic metadata lookup and quality verification.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

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
A: No, this tool is for audio CDs only. For DVDs, use tools like HandBrake or MakeMKV.

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

**Happy Ripping! 💿**
