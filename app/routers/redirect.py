from fastapi import APIRouter, Path, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from app.models import URL

router = APIRouter(tags=["Redirect URL"])


@router.get("/{key}", response_class=RedirectResponse, status_code=status.HTTP_200_OK)
async def redirect(key: str = Path(max_length=6)):
    """
    Redirect the target URL associated with the provided key.

    :param key: The key associated with the URL.
    :return: A redirect response to the target URL if it exists; raises a 404 error if not found.
    """
    exist_url = await URL.filter(key=key).first()

    if exist_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This URL Key does not exist."
        )

    if not exist_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The URL is deactivated by owner"
        )

    exist_url.clicks += 1
    await exist_url.save()

    return RedirectResponse(exist_url.url)
