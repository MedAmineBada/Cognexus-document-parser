from typing import List

import httpx
from httpx import ConnectError, TimeoutException

from api.v1.utils.exceptions import BadGatewayException, GatewayTimeoutException, CustomException
from config import env


async def upload_images(files: List[str], folder: str):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                env.EXGATE_CLOUDINARY_URL,
                json={"folder":folder, "files":files}
            )

    except ConnectError:
        raise BadGatewayException(message="Failed to connect to LLMOrc service.")
    except TimeoutException:
        raise GatewayTimeoutException(message="LLMOrc service timed out.")

    if response.status_code != 200:
        try:
            body = response.json()
            message = body.get("error") or "Something went wrong within the LLMOrc Service."
        except Exception:
            message = "Something went wrong within the LLMOrc Service."

        raise CustomException(status_code=response.status_code,message=message)

    return response.json()
