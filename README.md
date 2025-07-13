# iMessage Image Extractor

This Python script extracts images from the iMessage database (`chat.db`) on macOS and converts them to PNG format, saving them to a designated folder. It processes all image attachments, including those not linked to specific messages or chats, and logs any issues for debugging.

## Features

- **Output Directory**: Creates `~/Desktop/iMessages_Images/` to store all extracted images.
- **Database Query**: Extracts all attachments with `mime_type` starting with `image/` (e.g., `image/jpeg`, `image/png`, `image/heic`).
- **Image Processing**:
  - Resolves file paths from the `filename` column in `chat.db` (e.g., `~/Library/Messages/Attachments/...`).
  - Uses the Pillow library to open images, convert them to RGB, and save as PNG.
  - Generates unique filenames (`image_{attachment_id}_{timestamp}.png`) to avoid conflicts.
- **Fallback**: If image conversion fails (e.g., corrupt image), the original file is copied.
- **Debugging**: Logs issues (e.g., missing files, conversion errors) to `debug_log.txt`.
- **No Chat Dependency**: Processes all image attachments, even those not linked to messages or chats.

## Prerequisites

- macOS system with iMessage database at `~/Library/Messages/chat.db`.
- Python 3 installed.
- Pillow library for image processing.

## Installation

1. **Install Pillow**:
   ```bash
   pip3 install Pillow
   ```

## Usage

1. **Save the Script**:
   - Save the script as `extract_imessage_images.py` in `~/Desktop/` (or another location, adjusting commands as needed).

2. **Verify Database and Attachments**:
   - Confirm the iMessage database exists:
     ```bash
     ls ~/Library/Messages/chat.db
     ```
   - Check for attachment files:
     ```bash
     ls -R ~/Library/Messages/Attachments/
     ```
   - Verify the number of image attachments in `chat.db`:
     ```bash
     sqlite3 ~/Library/Messages/chat.db "SELECT COUNT(*) FROM attachment WHERE mime_type LIKE 'image/%'"
     ```
     This displays the total number of images to be extracted.

3. **Run the Script**:
   - Navigate to the script's directory:
     ```bash
     cd ~/Desktop
     ```
   - Execute the script:
     ```bash
     python3 extract_imessage_images.py
     ```
   - The script will:
     - Create `~/Desktop/iMessages_Images/` for output.
     - Save images as PNG files named `image_{attachment_id}_{timestamp}.png`.
     - Generate `debug_log.txt` for any issues.

4. **Check Output**:
   - Open `~/Desktop/iMessages_Images/` to view extracted images.
   - Expected structure:
     ```
     ~/Desktop/iMessages_Images/
     ├── image_123_20250712_212305_123456.png
     ├── image_124_20250712_212306_654321.png
     ├── debug_log.txt
     ```
   - Open images in Preview to verify.

5. **Review Debug Log**:
   - Check `~/Desktop/iMessages_Images/debug_log.txt` for any issues, such as:
     ```
     Attachment ID 125: File not found at ~/Library/Messages/Attachments/...
     Attachment ID 126: Failed to convert/save image: Corrupt image
     Processed 100 images, skipped 5 images
     ```

## Notes

- Ensure you have read permissions for `~/Library/Messages/chat.db` and `~/Library/Messages/Attachments/`.
- The script handles all image types supported by Pillow (e.g., JPEG, PNG, HEIC).
- If the script skips images, check `debug_log.txt` for details on missing or corrupt files.
- For large attachment sets, the script may take time to process.

## Contributing

Feel free to submit issues or pull requests to improve the script. Suggestions for additional features or optimizations are welcome!

## License

This project is licensed under the MIT License.
