import os
import random
from typing import Tuple
from aiohttp import FormData
from barazmoon import BarAzmoon

URL = "http://192.168.49.2:30512/predict"
IMG_DIR = "imagenet-sample-images"

# collect images
files = [
    os.path.join(IMG_DIR, f)
    for f in os.listdir(IMG_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not files:
    raise Exception("No images found")

print(f"Loaded {len(files)} images")


class MyLoadTester(BarAzmoon):

    def get_request_data(self) -> Tuple[str, FormData]:
        file_path = random.choice(files)

        form = FormData()
        form.add_field(
            "file",
            open(file_path, "rb"),
            filename=os.path.basename(file_path),
            content_type="image/jpeg",
        )

        return file_path, form

    def process_response(self, data_id: str, response: dict):
        # you can add latency parsing later if needed
        print(f"{data_id} -> OK")
        return True


# workload = requests per second
with open("workload.txt", "r") as f:
    content = f.read()


workload_list = [int(x) for x in content.split()]
if __name__ == "__main__":
    tester = MyLoadTester(
        workload=workload_list,
        endpoint=URL,
        http_method="post"
    )

    total, success = tester.start()

    print("\n--- SUMMARY ---")
    print(f"Total requests: {total}")
    print(f"Successful: {success}")