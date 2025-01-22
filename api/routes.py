from fastapi import APIRouter, HTTPException #FastAPI
from typing import Dict, Any
from pydantic import BaseModel
from typing import List
from http import HTTPStatus
from services.workflow import Agent
from db.db import Vectorize

router = APIRouter()
agent = Agent()
agent.compile()

class URLList(BaseModel):
    urls: List[str]

@router.post('/admin/insert/')
def insert(url_list: URLList):
    try:
        vtr_obj = Vectorize()
        #vtr_obj.client_setup()
        vtr_obj.chunker(url_list.urls)
        flag = vtr_obj.store()
        if flag:
            return {"message": "Data updated in VectorDB"}
        else:
            return {"error": "Data failed to update in VectorDB"}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post('/agent/query/')
async def query(request: Dict[str, Any]):
    try:
        output = agent.run(request)
        return { "answer": output }
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))