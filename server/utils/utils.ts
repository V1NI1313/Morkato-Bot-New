import { Json, JsonArray } from "./types";

export function getitem(obj: Json | JsonArray | any, key: string | number, value: any=null): any {
  if (obj[key] !== undefined) {return obj[key]} else {return value;}
}