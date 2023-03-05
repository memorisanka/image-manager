from PIL import Image as PillowImage


def generate_thumbnail(image_path, thumbnail_path, size):
    with PillowImage.open(image_path) as img:
        img.thumbnail((size, size))
        img.save(thumbnail_path)
