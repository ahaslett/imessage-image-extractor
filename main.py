import sqlite3
import os
import shutil
from PIL import Image
import mimetypes
from datetime import datetime

# Define output directory
output_dir = os.path.expanduser("~/Desktop/iMessages_Images")
os.makedirs(output_dir, exist_ok=True)

# Debug log file
debug_log_path = os.path.join(output_dir, "debug_log.txt")
debug_log = open(debug_log_path, 'w', encoding='utf-8')

# Connect to the Messages database
db_path = os.path.expanduser("~/Library/Messages/chat.db")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
except sqlite3.Error as e:
    debug_log.write(f"Error connecting to database: {e}\n")
    print(f"Error: Could not connect to chat.db: {e}")
    debug_log.close()
    exit(1)

# Query all attachments with image MIME types
cursor.execute("""
    SELECT ROWID, filename, mime_type
    FROM attachment
    WHERE mime_type LIKE 'image/%'
""")
attachments = cursor.fetchall()

# Counters
processed_images = 0
skipped_images = 0

# Process attachments
for attachment in attachments:
    attachment_id, filename, mime_type = attachment
    
    # Skip if filename is missing
    if not filename:
        debug_log.write(f"Attachment ID {attachment_id}: No filename\n")
        skipped_images += 1
        continue
    
    # Resolve attachment path
    attachment_path = os.path.expanduser(filename)
    if not os.path.exists(attachment_path):
        debug_log.write(f"Attachment ID {attachment_id}: File not found at {attachment_path}\n")
        skipped_images += 1
        continue
    
    # Generate output filename (use timestamp to avoid conflicts)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_filename = f"image_{attachment_id}_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)
    
    # Convert and save as PNG
    try:
        with Image.open(attachment_path) as img:
            img.convert("RGB").save(output_path, "PNG")
        processed_images += 1
    except Exception as e:
        debug_log.write(f"Attachment ID {attachment_id}: Failed to convert/save image: {e}\n")
        # Fallback: Copy original file if conversion fails
        try:
            shutil.copy(attachment_path, output_path)
            debug_log.write(f"Attachment ID {attachment_id}: Copied original file as fallback\n")
            processed_images += 1
        except (OSError, shutil.Error) as e:
            debug_log.write(f"Attachment ID {attachment_id}: Fallback copy failed: {e}\n")
            skipped_images += 1
            continue

# Clean up
debug_log.write(f"Processed {processed_images} images, skipped {skipped_images} images\n")
debug_log.close()
conn.close()

print(f"Export complete. Images saved in {output_dir}")
print(f"Processed {processed_images} images, skipped {skipped_images} images")
print(f"Check {debug_log_path} for details on skipped images")
