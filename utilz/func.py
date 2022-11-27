from typing import (Optional, Union, Any)
import requests
import json

class Route:
  url: str = "http://localhost:5500"
  
  @classmethod
  def get(
    cls,
    local: str,
    **kwgs
  ) -> requests.Response:
    url = f"{cls.url}{f'/`{local}' if not local[0]=='/' else local}"
    return requests.get(url, **kwgs)
  @classmethod
  def post(
    cls,
    local: str,
    data: Union[str, int, dict, bytes],
    headers: Optional[dict[str, Union[str, int, bool]]]=...
  ) -> requests.Response:
    url = f"{cls.url}{f'/{local}' if not local[0]=='/' else local}"
    _headers = (
      headers
      if not headers is ...
      else {
        "content-type": "application/json"
      }
    )
    _data = (
      data
      if not isinstance(data, dict)
      else json.dumps(data)
    )
    return requests.post(url, data=_data, headers=_headers)
  @classmethod
  def patch(
    cls,
    local: str,
    data: Union[str, int, dict, bytes],
    headers: Optional[dict[str, Union[str, int, bool]]]=...
  ) -> requests.Response:
    url = f"{cls.url}{f'/{local}' if not local[0]=='/' else local}"
    _headers = (
      headers
      if not headers is ...
      else {
        "content-type": "application/json"
      }
    )
    _data = (
      data
      if not isinstance(data, dict)
      else json.dumps(data)
    )
    return requests.patch(url, data=_data, headers=_headers)
    
    