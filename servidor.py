# tener en cuenta para hacer uso de Run Cell
# https://pypi.org/project/ipykernel/
# en la maquina virtual Venv

# %% 


import asyncio
import http
import signal


import websockets
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np




async def send_data(websocket, path):
    data_2=[]
    while True:
            # Recibir datos del cliente
            data = await websocket.recv()
            # Convertir los datos a una lista de enteros
            data = list(map(int, data.split(',')))

            #print("****** Unimos los datos que envia el cliente la cual representario los 8 sensores *****")
            data_2.append(data)
            #print(data_2)
            #print("****************************************************************************************")

            # cada columna represente un sensor a graficar
            #print("******* DF *****")
            df_concadenados=pd.DataFrame(data_2, columns=["0", "1", "2","3","4","5","6","7"])
            #print(df_concadenados)

            #print("*** Dimencion de la matriz ***")
            #print(df_concadenados.shape)
            dimencion=df_concadenados.shape[0]
            print(dimencion)

            #print("*** Nombre de las columnas de la matriz ***")
            #print(df_concadenados.columns)

            #print("** Tipos de datos si se encuentran enteros los pasamos a float64**")

            #print(df_concadenados.dtypes)
            df_concadenados['0'] = df_concadenados['0'].astype('float64')
            df_concadenados['1'] = df_concadenados['1'].astype('float64')
            df_concadenados['2'] = df_concadenados['2'].astype('float64')
            df_concadenados['3'] = df_concadenados['3'].astype('float64')
            df_concadenados['4'] = df_concadenados['4'].astype('float64')
            df_concadenados['5'] = df_concadenados['5'].astype('float64')
            df_concadenados['6'] = df_concadenados['6'].astype('float64')
            df_concadenados['7'] = df_concadenados['7'].astype('float64')

            # print("** Tipos de datos **")
            # print(df_concadenados.dtypes)

            #print("*** Nombre de las columnas de la matriz ***")
            #print(df_concadenados.columns)

            dimencion_x = np.linspace(0, dimencion, dimencion)
            #print("************")
            #print(dimencion_x)
            #print("************")

            # -----------------------------------
            # Graficar los datos
            # -----------------------------------

            plt.plot(dimencion_x, df_concadenados['0'], marker = 'o', label='1')
            plt.plot(dimencion_x, df_concadenados['1'], marker = 'o', label='2')
            plt.plot(dimencion_x, df_concadenados['2'], marker = 'o', label='3')
            plt.plot(dimencion_x, df_concadenados['3'], marker = 'o', label='4')
            plt.plot(dimencion_x, df_concadenados['4'], marker = 'o', label='5')
            plt.plot(dimencion_x, df_concadenados['5'], marker = 'o', label='6')
            plt.plot(dimencion_x, df_concadenados['6'], marker = 'o', label='7')
            plt.plot(dimencion_x, df_concadenados['7'], marker = 'o', label='8')


            plt.xlabel('Eje X')
            plt.ylabel('Eje Y')
            plt.title("Grafica de los sensores")
            plt.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
                        
            plt.pause(0.05)
            plt.clf()
            plt.show()
            print("fin")

            message = (f"El servidor responde: \n {df_concadenados}")
            await websocket.send(message)
            
                  
async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        send_data,
        host="",
        port=8080,
        process_request=health_check,
    ):
        await stop

if __name__ == "__main__":
    asyncio.run(main())