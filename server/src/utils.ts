interface JsonArray extends Array<string|number|boolean|Date|Json|JsonArray> { }
interface Json {[x: string]: string|number|boolean|Date|Json|JsonArray;}

interface dict<T> extends RelativeIndexable<T> {
  constructor: Function,
  json: Json | JsonArray,
  length: number,
  get: (key: string, value?: any | null)=>{},
  [key: string]: any
}
export namespace pythonObjects{
  export class dictionary<T> {
    public obj: Json | JsonArray | any = {};
    constructor(source: Json | JsonArray) {
      this.obj = source
    }
    public get(key: string, value: any | null=null): T {
      let _value = this.obj[key]
      if (_value !== undefined) {return _value;}
      else {return value;}
    }
    public getitem(key: string): T {return this.obj[key];}
  }
}
export function getitem(obj: Json | JsonArray | any, key: string | number, value: any=null) {
  if (obj[key] !== undefined) {return obj[key]} else {return value;}
}