from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from script import get_points, blend_images, opencv_to_pillow, pillow_to_base64, base64_to_opencv

app_api = FastAPI()


class RequestData(BaseModel):
    image: str
    alpha: Optional[float] = 0.7


class ResponseData(BaseModel):
    pass


@app_api.post('/api/auto_flag')
async def auto_tag(data: RequestData):
    image = base64_to_opencv(data.image)
    points = get_points(image)
    output = blend_images(opencv_to_pillow(image), points, data.alpha)

    return {'image': pillow_to_base64(output)}
