from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.exceptions import AppException


async def app_exception_handler(request: Request, exception: AppException):
	return JSONResponse(
		status_code=exception.status_code,
		content={
			"success": False,
			"error": {
				"message": exception.message,
				"type": exception.__class__.__name__,
				"path": request.url.path,
			},
		},
	)
