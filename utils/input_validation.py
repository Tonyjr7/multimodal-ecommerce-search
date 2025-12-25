# Add validation helper
def validate_image_file(file):
    """
    Validate uploaded image file.
    """
    if not file:
        return False, "No file provided"
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    filename = file.filename.lower()
    if not any(filename.endswith(f'.{ext}') for ext in allowed_extensions):
        return False, "Invalid file type"
    
    # Check file size (additional check)
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset
    
    if size > 10 * 1024 * 1024:  # 10MB
        return False, "File too large"
    
    return True, None