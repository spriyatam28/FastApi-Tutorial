from pydantic import BaseModel
from starlette.responses import JSONResponse
from fastapi import status


class BaseResponse(BaseModel):
	result: str

	@staticmethod
	def response(result: bool) -> JSONResponse:
		"""Returns a base JSONResponse using the model"""
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content={
				"successful": result,
			},
		)
