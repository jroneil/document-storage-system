from PIL import Image

def generate_thumbnail(image_path: str, output_path: str, size: tuple = (128, 128)) -> str:
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(output_path)
            return output_path
    except Exception as e:
        raise Exception(f"Failed to generate thumbnail: {str(e)}")