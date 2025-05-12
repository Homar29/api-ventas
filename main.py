from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io

app = FastAPI()

@app.post("/procesar")
async def procesar_excel(archivo_excel: UploadFile = File(...)):
    content = await archivo_excel.read()
    xls = pd.read_excel(io.BytesIO(content), sheet_name=None)

    resumen = []

    for nombre_mes, df in xls.items():
        columnas_esperadas = [
            "Unidades vendidas", "Precio total", "Costo de envío",
            "Costo de envío a tu cargo", "Comisión de Mercado Libre", "Te queda"
        ]
        # Si la hoja tiene columnas válidas, la procesamos
        if any(col in df.columns for col in columnas_esperadas):
            fila = {"mes": nombre_mes}
            fila["unidades_vendidas"] = df.get("Unidades vendidas", pd.Series(dtype=float)).sum()
            fila["precio_total"] = df.get("Precio total", pd.Series(dtype=float)).sum()
            fila["costo_envio"] = df.get("Costo de envío", pd.Series(dtype=float)).sum()
            fila["costo_envio_a_tu_cargo"] = df.get("Costo de envío a tu cargo", pd.Series(dtype=float)).sum()
            fila["comision_mercado_libre"] = df.get("Comisión de Mercado Libre", pd.Series(dtype=float)).sum()
            fila["te_queda"] = df.get("Te queda", pd.Series(dtype=float)).sum()
            resumen.append(fila)

    return {"resumen": resumen}
