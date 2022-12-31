export interface JsonArray extends Array<string|number|boolean|Date|Json|JsonArray|any> { }
export interface Json {[x: string]: string|number|boolean|Date|Json|JsonArray|any;}
export interface embed {
  title: string|null,
  description: string|null,
  url: string|null
}