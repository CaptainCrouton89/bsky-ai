from io import BytesIO

import requests
from PIL import Image


def download_image_data(image_url, max_size_kb, output_format="JPEG"):
    print(image_url)
    try:
        # Step 1: Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        image = Image.open(BytesIO(response.content))
        # decrease image dimensions
        while True:
            if image.size[0] * image.size[1] / 1024 < max_size_kb:
                break
            else:
                image = image.resize((image.size[0] // 2, image.size[1] // 2))

        output_buffer = BytesIO()
        output_buffer.seek(0)  # Reset buffer
        image.save(output_buffer, format=output_format, quality=95)
        return output_buffer.getvalue()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None