from __future__ import annotations

from . import utils
import requests
import json
import re

T = utils.TypeVar('T')
class Route:
  url: str = "http://localhost:5500"
  
  @classmethod
  def get(
    cls,
    local: str, /,
    **kwgs
  ) -> requests.Response:
    url = f"{cls.url}{f'/`{local}' if not local[0]=='/' else local}"
    return requests.get(url, **kwgs)
  @classmethod
  def post(
    cls,
    local: str, /,
    data: utils.Union[str, int, dict, bytes],
    headers: utils.Optional[dict[str, utils.Union[str, int, bool]]]=...
  ) -> requests.Response:
    url = f"{cls.url}{f'/{local}' if not local[0]=='/' else local}"
    _headers = (
      headers
      if not headers is ...
      else {
        "content-type": "application/json"
      }
    )
    if isinstance(data, dict):
      _data = json.dumps(data)
    return requests.post(url, data=_data, headers=_headers)
  @classmethod
  def patch(
    cls,
    local: str, /,
    data: utils.Union[str, int, dict, bytes],
    headers: utils.Optional[dict[str, utils.Union[str, int, bool]]]=...
  ) -> requests.Response:
    url = f"{cls.url}{f'/{local}' if not local[0]=='/' else local}"
    _headers = (
      headers
      if not headers is ...
      else {
        "content-type": "application/json"
      }
    )
    if isinstance(data, dict):
      _data = json.dumps(data)
    return requests.patch(url, data=_data, headers=_headers)
  @classmethod
  def delete(
    cls,
    local: str, /
  ) -> requests.Response:
    url = f"{cls.url}{f'/{local}' if not local[0]=='/' else local}"
    return requests.delete(url)
def getAll(array: list, obj: object) -> list:
  return [i for i in array if i == obj]
class Decimals(utils.Generic[T]):
  def __init__(self, num: T) -> None:
    self.value: T = num
  def __repr__(self) -> str:
    return str(self.value)
  def __add__(self, n: T) -> utils.Generic[T]:
    return Decimals(self.value+n)
  def normalize(self) -> Decimals:
    if isinstance(self.value, int):
      return Decimals(self.value)
    normalized = round(self.value, 2)
    normalized = str(normalized).strip('0').strip('.')
    return Decimals(eval(normalized))
  def parseInt(self) -> Decimals:
    return Decimals(round(self.value))
  def normalizeString(self) -> str:
    if isinstance(self.value, float):
      value = self.normalize()
    else:
      value = self.value
    if value < 1000:
      return value
    elif value >= 1000 and value < 1000000:
      value = str(Decimals(value/1000).normalize()).strip('0').strip('.')
      return f"{value}k"
def setDictOptional(obj: dict, key: str, value: utils.Any) -> dict:
  if value is None:
    return obj
  obj[key] = value
  return obj