import pytest
import requests
import base64

def test_remove_image_watermark(setup):
    with open("1.png", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    res = requests.post(
        "http://localhost:5000/RemoveImageWatermark",
        json={"sourceURI": f"data:image/png;base64,{image_base64}"}
    )
    targetURI = res.json()["targetURI"]
    assert targetURI.startswith("data:image/png;base64,")

    with open("2.png", "wb") as f:
        f.write(base64.b64decode(targetURI.split(",")[1]))
