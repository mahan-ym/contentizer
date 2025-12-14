import os
import requests
from dotenv import load_dotenv
import time
import base64
from src.services.uuid import gen_uuid_str
from src.global_constants import ASSETS_DIR
from src.shared_state import SharedState

_shared_state = SharedState()


# get from environment variables
load_dotenv()
FREEPIK_API_KEY = os.getenv("FREEPICK_KEY")
BASE_URL = "https://api.freepik.com/v1"

timeout = 600  # 10 minutes


def gen_vid(
    prompt: str = "",
    negative_prompt: str = "",
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
        prompt (str): The prompt to guide the video generation.
        negative_prompt (str): The negative prompt to avoid certain elements in the video.
        duration (int): The duration of the generated video in seconds. Default is 5. options: 5, 10

    Returns:
        str: The absolute path to the generated video file, or None if generation failed.
    """

    image = _shared_state.get_image_path()
    if image:
        print(f"[gen_vid] Using image from shared state: {image}")
    else:
        print("[gen_vid] Warning: No image found in shared state")
        print(f"[gen_vid] _shared_state object: {_shared_state}")
        print(f"[gen_vid] _shared_state.__dict__: {_shared_state.__dict__}")
        return None

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
            generated_list = response.json()["data"].get("generated")
            if not generated_list:
                print("[gen_vid] Error: No generated video URLs in response")
                return None
            VIDEO_URL = generated_list[0]
            video_uuid = gen_uuid_str()
            video_path = os.path.join(ASSETS_DIR, video_uuid)
            os.makedirs(video_path, exist_ok=True)
            file_name = os.path.join(video_path, f"{video_uuid}.mp4")
            video_response = requests.get(VIDEO_URL)
            if video_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(video_response.content)
                print(f"Video successfully downloaded as {file_name}")
                # Store video path in shared state
                if _shared_state is not None:
                    _shared_state.set_video_path(file_name)
                return file_name
            else:
                print(
                    f"Could not download the video. Status code: {video_response.status_code}"
                )
                return None
    else:
        print(
            f"Error while generating the video. Status code: {response.status_code}, message: {response.json()['message']}"
        )
        return None


def gen_image(
    prompt: str,
    aspect_ratio: str = "widescreen_16_9",
):
    """
    Generate an image from a text prompt and save it with a unique UUID.

    Returns the file path of the generated image for use in video generation.

    args:
        prompt (str): The prompt to guide the image generation.
        aspect_ratio (str): The aspect ratio of the generated image.
            Available options: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_post_4_5
            Example: "widescreen_16_9"

    returns:
        str: The absolute path to the generated image file, or None if generation failed.
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
            status_url = f"{BASE_URL}/ai/text-to-image/flux-pro-v1-1/{task_id}"
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

            # Generate unique ID and create assets directory structure
            image_uuid = gen_uuid_str()

            assets_dir = os.path.join(ASSETS_DIR, image_uuid)
            os.makedirs(assets_dir, exist_ok=True)

            file_name = os.path.join(assets_dir, f"{image_uuid}.jpeg")
            image_response = requests.get(IMAGE_URL)
            if image_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(image_response.content)
                print(f"Image successfully downloaded as {file_name}")
                # Store image path in shared state
                print(
                    f"[gen_image] About to store image path in SharedState (ID: {id(_shared_state)})"
                )
                if _shared_state is not None:
                    _shared_state.set_image_path(file_name)
                    print(
                        f"[gen_image] After storing, state is: {_shared_state.__dict__}"
                    )
                return file_name
            else:
                print(
                    f"Could not download the image. Status code: {image_response.status_code}"
                )
                return None
    else:
        print(
            f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}"
        )
        return None
