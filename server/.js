let lista = []
while(true) {
  let k = Math.floor(Math.random() * 1000000000000000000000)
  if(k in lista) {
    console.log("tentativas: " + lista.length.toString() + " Número: " + k.toString()); break
  }; lista.push(k)
}