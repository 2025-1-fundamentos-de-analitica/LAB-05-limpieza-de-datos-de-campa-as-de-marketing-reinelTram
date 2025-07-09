"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile
import pandas as pd
from glob import glob
def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months

    """

    """
    Limpia y transforma los datos de una campaña de marketing bancaria.
    Procesa archivos CSV comprimidos en ZIP desde 'files/input/' y genera
    tres archivos CSV limpios en 'files/output/'.
    """


    """
    Limpia y transforma los datos de una campaña de marketing bancaria.
    Procesa archivos CSV comprimidos en ZIP desde 'files/input/' y genera
    tres archivos CSV limpios en 'files/output/'.
    """

    input_dir = "files/input/"
    output_dir = "files/output/"
    os.makedirs(output_dir, exist_ok=True)

    dfs = []
    for zip_path in glob(os.path.join(input_dir, "*.zip")):      
        with zipfile.ZipFile(zip_path, "r") as z:
            for file_name in z.namelist():
                if file_name.endswith(".csv"):                   
                    with z.open(file_name) as f:
                        df = pd.read_csv(f, sep=",", encoding="utf-8")
                        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)
  

    # CLIENT
    client = pd.DataFrame()
    client["client_id"] = data["client_id"]
    client["age"] = data["age"]
    client["job"] = data["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["marital"] = data["marital"]
    client["education"] = data["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = data["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client["mortgage"] = data["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)
   

    # CAMPAIGN
    campaign = pd.DataFrame()
    campaign["client_id"] = data["client_id"]
    campaign["number_contacts"] = data["number_contacts"]
    campaign["contact_duration"] = data["contact_duration"]
    campaign["previous_campaign_contacts"] = data["previous_campaign_contacts"]
    campaign["previous_outcome"] = data["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = data["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)

    # Día y mes → fecha
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    day = data["day"].astype(str).str.zfill(2)
    month = data["month"].map(month_map)
    campaign["last_contact_date"] = "2022-" + month + "-" + day
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    

    # ECONOMICS
    economics = pd.DataFrame()
    economics["client_id"] = data["client_id"]
    economics["cons_price_idx"] = data["cons_price_idx"]
    economics["euribor_three_months"] = data["euribor_three_months"]
    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)
 

if __name__ == "__main__":
    clean_campaign_data()


