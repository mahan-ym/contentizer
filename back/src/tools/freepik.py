import os
import requests
from dotenv import load_dotenv
from PIL.Image import Image
import time
import base64


# get from environment variables
load_dotenv()
FREEPIK_API_KEY = os.getenv("FREEPICK_KEY")
BASE_URL = "https://api.freepik.com/v1"

timeout = 600  # 10 minutes


def gen_vid(
    image: str,
    prompt: str,
    negative_prompt: str,
    duration: int = 5,
):
    """
    This tool generate video from and image using prompt and negative prompt.

    While the task is being processed the return is:
        Waiting for the task to complete... (current status: IN_PROGRESS)
    When the task is completed the return is:
        COMPLETED
        Video successfully downloaded as /path/to/generated_video.mp4

    Args:
        image (str): The input image url or image path.
        prompt (str): The prompt to guide the video generation.
        negative_prompt (str): The negative prompt to avoid certain elements in the video.
        duration (int): The duration of the generated video in seconds. Default is 5. options: 5, 10
    """
    endpoint = f"{BASE_URL}/ai/image-to-video/kling-v2-5-pro"

    headers = {
        "x-freepik-api-key": f"{FREEPIK_API_KEY}",
        "Content-Type": "application/json",
    }

    # prepare image payload
    if image.startswith("http://") or image.startswith("https://"):
        pass  # image is already a URL
    else:
        # assume image is an image path and should be converted to base64 string
        with open(image, "rb") as image_file:
            image = "data:image/jpeg;base64," + base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    payload = {
        "image": image,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "duration": str(duration),
        "cfg_scale": 0.5,
    }

    start_time = time.time()
    generation_ok = True
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        task_id = response.json()["data"]["task_id"]
        status = response.json()["data"]["status"]

        # Polling until the status is "COMPLETED"
        while status != "COMPLETED":
            print(f"Waiting for the task to complete... (current status: {status})")
            time.sleep(2)  # Wait 2 seconds before checking again
            status_url = (
                f"https://api.freepik.com/v1/ai/image-to-video/kling-v2-5-pro/{task_id}"
            )
            response = requests.get(
                status_url,
                headers={"x-freepik-api-key": f"{FREEPIK_API_KEY}"},
            )
            if response.status_code == 200:
                status = response.json()["data"]["status"]
            else:
                print(f"Error while checking the task status: {response.status_code}")
                time.sleep(2)
            if time.time() - start_time > timeout:
                print("Timeout reached")
                generation_ok = False
                break

        if generation_ok:
            print("COMPLETED")
            # Download the video ---------------------------------------------------------------
            VIDEO_URL = response.json()["data"]["generated"][0]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(current_dir, "generated_video.mp4")
            video_response = requests.get(VIDEO_URL)
            if video_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(video_response.content)
                print(f"Video successfully downloaded as {file_name}")
            else:
                print(
                    f"Could not download the video. Status code: {video_response.status_code}"
                )
    else:
        print(
            f"Error while generating the video. Status code: {response.status_code}, message: {response.json()['message']}"
        )


def gen_image(
    prompt: str,
    aspect_ratio: str = "square_1_1",
):
    """
    
    args:
        prompt (str): The prompt to guide the image generation.
        aspect_ratio (str): The aspect ratio of the generated image. 
            Available options: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_post_4_5 
            Example: "square_1_1"
    """
    endpoint = f"{BASE_URL}/ai/text-to-image/flux-pro-v1-1"
    headers = {
        "x-freepik-api-key": f"{FREEPIK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "prompt_upsampling": True,
        "aspect_ratio": aspect_ratio,
        "safety_tolerance": 2,
        "output_format": "jpeg",
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        task_id = response.json()["data"]["task_id"]
        status = response.json()["data"]["status"]

        start_time = time.time()
        generation_ok = True
        # Polling until the status is "COMPLETED"
        while status != "COMPLETED":
            print(f"Waiting for the task to complete... (current status: {status})")
            time.sleep(2)  # Wait 2 seconds before checking again
            status_url = (
                f"{BASE_URL}/ai/text-to-image/flux-pro-v1-1/{task_id}"
            )
            response = requests.get(
                status_url,
                headers={"x-freepik-api-key": f"{FREEPIK_API_KEY}"},
            )
            if response.status_code == 200:
                status = response.json()["data"]["status"]
            else:
                print(f"Error while checking the task status: {response.status_code}")
                time.sleep(2)
            if time.time() - start_time > timeout:
                print("Timeout reached")
                generation_ok = False
                break

        if generation_ok:
            print("COMPLETED")
            # Download the image ---------------------------------------------------------------
            IMAGE_URL = response.json()["data"]["generated"][0]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(current_dir, "generated_image.jpeg")
            image_response = requests.get(IMAGE_URL)
            if image_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(image_response.content)
                print(f"Image successfully downloaded as {file_name}")
            else:
                print(
                    f"Could not download the image. Status code: {image_response.status_code}"
                )
    else:
        print(
            f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}"
        )




if __name__ == "__main__":
    # image_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
    # current_dir = os.path.dirname(os.path.abspath(__file__))

    # gen_vid(
    #     image= os.path.join(current_dir, "s-bg3.jpg"),
    #     prompt="create a shock and make the stones float into the sky. create a blue light around the stones when they are floated.",
    #     negative_prompt="blurry, low resolution, dark, gloomy, cartoon",
    #     duration=5,
    # )

    gen_image(
        prompt="A Beautiful animated wrench flying toward the a bolt to fasten it, high detail, vibrant colors, dynamic lighting, dramatic angle, digital art",
        aspect_ratio="widescreen_16_9",
    )
