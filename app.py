import pandas as pd

import requests


import json

import re
 
# Load your CSV

with open("custom_crawl_output_0_62_6.csv", "r", encoding="utf-8", errors="ignore") as f:

    lines = f.readlines()
 
# input('hloooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
records = []

for line in lines:

    page_type_match = re.search(r'"page_type":\s*"([^"]+)"', line)

    page_text_match = re.search(r'"page_text":\s*"([^"]+)"', line)
 
    page_type = page_type_match.group(1) if page_type_match else None

    page_text = page_text_match.group(1) if page_text_match else None
 
    if page_type == "contact":

        records.append({"page_type": page_type, "page_text": page_text})
 
contact_df = pd.DataFrame(records)
 
def extract_contact_info(page_text):

    prompt = f"""

    You are an AI data extractor. Extract 100% accurate structured data from the following contact page text.

    Return output strictly as JSON with these fields:

    name, email, contact, full address.
 
    If any field is missing, set it to null.
 
    TEXT:

    {page_text}

    """
 
    response = requests.post(
    "http://your-local-ip:11434/api/generate",
    json={"model": "llama3.1", "prompt": "Hello"}
)

data = response.json()
st.write(data["response"])

 
    try:


        result_text = response["message"]["content"]

        print("result_text:::::::::::::::", result_text)

        return json.loads(result_text)

    except Exception:

        return {"name": None, "email": None, "contact": None, "address": None}
 

results = []

for _, row in contact_df.iterrows():

    data = extract_contact_info(row["page_text"])

    results.append({

        "page_url": row.get("page_url", ""),

        "name": data["name"],

        "email": data["email"],

        "contact": data["contact"],

        "address": data.get("address",''),

    })
 

output_df = pd.DataFrame(results)
 

output_df.to_csv("extracted_contact_infobro.csv", index=False)
 
print("✅ Extraction complete. Saved to extracted_contact_infobro.csv")
 
