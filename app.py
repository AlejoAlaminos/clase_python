from fastapi import FastAPI, Body, Path, Query

app = FastAPI()

app.title = "Tienda de juegos"

productos = [
    {"id": 1, "nombre": "The Legend of Zelda: Breath of the Wild", "precio": 59.99, "activo": True},
    {"id": 2, "nombre": "Super Mario Odyssey", "precio": 49.99, "activo": True},
    {"id": 3, "nombre": "Minecraft", "precio": 26.95, "activo": True},
    {"id": 4, "nombre": "League of Legends", "precio": 0.00, "activo": True},
    {"id": 5, "nombre": "Call of Duty: Modern Warfare", "precio": 59.99, "activo": True}
]        

@app.get("/productos")
async def get_productos():
    return productos

@app.get("/productos/{id}")
async def get_producto_by_id(
    id: int = Path(..., description="El ID del producto a obtener")):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return {"error": "Producto no encontrado"}

@app.post("/productos")
async def crear_producto(
    id: int = Body(gt=0),
    nombre: str = Body(min_length=1, description="El nombre del producto"),
    precio: float = Body(ge=0, lt= 99999, description="El precio del producto"),
    activo: bool = Body(..., description="Indica si el producto está activo")):
    nuevo_producto = {
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "activo": activo
    }
    productos.append(nuevo_producto)
    return nuevo_producto

@app.put("/productos/{id}")
async def actualizar_producto(
    id: int = Path(gt=0, description="El ID del producto a actualizar"),
    nombre: str = Body(min_length=1, description="El nuevo nombre del producto"),
    precio: float = Body(ge=0, lt=99999, description="El nuevo precio del producto"),
):
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = nombre
            producto["precio"] = precio
            return producto
    return {"error": "Producto no encontrado"}

@app.delete("/productos/{id}")
async def eliminar_produtcto(
    id: int,
    logico: bool = Query(description="Si es true, se desactiva el producto en lugar de eliminarlo", default =False)
):
    for producto in productos:
        if producto["id"] == id:
            if logico:
                producto["activo"] = False
                return {"mensaje": "Producto desactivado"}
            else:
                productos.remove(producto)
                return {"mensaje": "Producto eliminado"}
    return {"error": "Producto no encontrado"}
