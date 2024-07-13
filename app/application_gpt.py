from typing import List

from cachetools import TTLCache
from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from pydantic import BaseModel
import logging
import math
import openai
from openai import OpenAI
import unidecode
import json5 as json

from app import config
from data.cnaes_list import cnaes
from vertexai.language_models import TextGenerationModel
import vertexai

router = APIRouter()

cache = TTLCache(maxsize=config.TTL_CACHE_MAXSIZE, ttl=config.TTL_CACHE_TTL)

logging.basicConfig(**config.LOGGING_CONFIG)

class InputData(BaseModel):
    cnae_number: str
    item_description: List[str]
    provider: str


openai.api_key = config.OPENAI_API_KEY
model = config.OPENAI_MODEL

client = OpenAI(
    api_key=openai.api_key
)

def classify_chatgpt(model, lista, cnae):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Abaixo temos uma lista de produtos extraídos de notas fiscais brasileiras.
                        Estes produtos foram comprados uma uma empresa do ramo de {cnae}.
                        {config.PROMPT}
                        Lista:
                        {lista}"""
                }
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        return [{'API Error': str(e)}]

def classify_product(request_json):

    if 'item_description' not in request_json or 'provider' not in request_json or "cnae_number" not in request_json:
        return {"Request Error": "Request did not have all necessary fields; 'item_description', 'cnae_number' and 'provider' (accepted: 'google') required"}

    cnae_number = request_json["cnae_number"].strip().zfill(7)  

    if not (6 <= len(cnae_number) <= 7):
        return {"Request Error": "Invalid 'cnae_number'. Field must only contain 7 numeric digits."}

    item_description = json.dumps(request_json["item_description"])
    #cache_key = f"{cnae_number}_{item_description}"

    #if cache_key in cache:
        #return cache[cache_key]

    try:
        cnae_ = cnaes[cnae_number]
    except KeyError:
        return {"Request Error": "Invalid 'cnae_number'. Value not found on CNAE list."}

    itens = request_json["item_description"]
    den, m= (8, model) if len(itens) <= 8 else (100 if len(itens) > 100 else len(itens), model)
    n = math.ceil(len(itens) / den)
    itens_ = [x.replace("'", "").replace('"', '') for x in itens]

    if request_json["provider"] != 'google':
        return {"Request Error": "Provider not recognized, only 'google' or 'azure' accepted."}

    general_response = []
    for x in range(n):
        slice_from = x * den
        slice_to = (x + 1) * den if x < n - 1 else None  
        response = classify_chatgpt(m, lista=itens_[slice_from:slice_to], cnae=cnae_)
        general_response.append(response)

    final_json = []
    for response in general_response:
        json_answer = json.loads(response)
        if 'products' in json_answer:
            final_json.extend(json_answer['products'])
        else:
            final_json.append(json_answer)

    for item in final_json:
        item['product'] = unidecode.unidecode(item['product'])
        item['type'] = unidecode.unidecode(item['type'])

    #cache[cache_key] = final_json

    return final_json

@router.get("/health")
def health() -> Response:
    logging.info("Received a request to /health endpoint")
    logging.info("Response: " + str(status.HTTP_200_OK))
    
    return Response(status_code=status.HTTP_200_OK)


@router.post("/classify_product")
async def main_classify_product(info: InputData) -> JSONResponse:
    logging.info("Received a request to /classify_product endpoint")
    logging.info("Input received: " + str(info))
    try:
        response = classify_product(info.dict())
        logging.info("Response: " + str(status.HTTP_200_OK) + " " + str(response))
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"query_result": response}
        )
    except ValueError as err:
        logging.info("Response: " + str(status.HTTP_400_BAD_REQUEST))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(err))
    except Exception as err:
        logging.info("Response: " + str(status.HTTP_500_INTERNAL_SERVER_ERROR))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Something wrong happened in the server side. {err}",
        )