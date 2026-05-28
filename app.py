from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()
app.title = "Tienda de juegos"


NOT_FOUND_RESPONSE = {
    404: {
        "description": "Producto no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Producto no encontrado"}
            }
        },
    }
}


IdProducto     = Annotated[int,   Field(gt=0,          description="ID del producto")]
NombreProducto = Annotated[str,   Field(min_length=1,  max_length=80, description="Nombre del producto")]
PrecioProducto = Annotated[float, Field(ge=0, lt=99999, description="Precio del producto")]
BoolActivo     = Annotated[bool,  Field(description="¿Sigue disponible?")]


class ProductoSchema(BaseModel):
    id:     IdProducto
    nombre: NombreProducto
    precio: PrecioProducto = 0.0
    activo: BoolActivo = True


class ProductoUpdateSchema(BaseModel):
    nombre: NombreProducto
    precio: PrecioProducto


productos = [
    {"id": 1, "nombre": "The Legend of Zelda: Breath of the Wild", "precio": 59.99, "activo": True},
    {"id": 2, "nombre": "Super Mario Odyssey",                      "precio": 49.99, "activo": True},
    {"id": 3, "nombre": "Minecraft",                                "precio": 26.95, "activo": True},
    {"id": 4, "nombre": "League of Legends",                        "precio":  0.00, "activo": True},
    {"id": 5, "nombre": "Call of Duty: Modern Warfare",             "precio": 59.99, "activo": True},
]



@app.get("/productos", response_model=list[ProductoSchema])
async def get_productos():
    return productos


@app.get(
    "/productos/{id}",
    response_model=ProductoSchema,
    responses=NOT_FOUND_RESPONSE,
)
async def get_producto_by_id(
    id: Annotated[int, Path(gt=0, description="ID del producto a obtener")],
):
    for producto in productos:
        if producto["id"] == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.post("/productos", response_model=list[ProductoSchema])
async def crear_producto(producto: ProductoSchema):
    productos.append(producto.model_dump())
    return productos


@app.put(
    "/productos/{id}",
    response_model=ProductoSchema,
    responses=NOT_FOUND_RESPONSE,
)
async def actualizar_producto(
    id:    Annotated[int, Path(gt=0, description="ID del producto a actualizar")],
    datos: ProductoUpdateSchema,
):
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = datos.nombre
            producto["precio"] = datos.precio
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.delete(
    "/productos/{id}",
    response_model=ProductoSchema,
    responses=NOT_FOUND_RESPONSE,
)
async def eliminar_producto(
    id:     Annotated[int,  Path(gt=0, description="ID del producto a eliminar")],
    logico: Annotated[bool, Query(description="Si es True, desactiva en lugar de eliminar")] = False,
):
    for producto in productos:
        if producto["id"] == id:
            if logico:
                producto["activo"] = False  # borrado lógico
            else:
                productos.remove(producto)  # borrado físico
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")
