import os
import weaviate
import pandas as pd
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from dotenv import load_dotenv

load_dotenv()

wcd_url = os.getenv("WEAVIATE_URL")
wcd_api_key = os.getenv("WEAVIATE_API_KEY")
openai_api_key = os.getenv("OPENAI_API")
cwd = os.getcwd()


def generate_chunks_and_metadata(file_path):
    df = pd.read_excel(file_path, header=0, usecols=lambda column: column != 0)
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)
    data_list = []
    for index, row in df.iterrows():
        # Construct the dictionary for each row
        data = {
            "row_id": row['show_id'],
            "metadata": {
                "country": row['country'] if pd.notna(row['country']) else '',
                "listed_in": row['listed_in'] if pd.notna(row['listed_in']) else '',
                "duration": row['duration'] if pd.notna(row['duration']) else '',
                "release_year": row['release_year'] if pd.notna(row['release_year']) else '',
                "type": row['type'] if pd.notna(row['type']) else ''
            },
            "text": {
                "title": row['title'] if pd.notna(row['title']) else '',
                "director": row['director'] if pd.notna(row['director']) else '',
                "description": row['description'] if pd.notna(row['description']) else '',
                "cast": row['cast'] if pd.notna(row['cast']) else ''
            }
        }

        data_list.append(data)
    return data_list


def ingest_data(data):
    weaviate_client = weaviate.connect_to_weaviate_cloud(cluster_url=wcd_url, auth_credentials=Auth.api_key(wcd_api_key), headers={"X-OpenAI-Api-Key": openai_api_key})
    if weaviate_client.is_ready():
        if not weaviate_client.collections.exists(name="netflix_data"):
            netflix_coll = weaviate_client.collections.create(name="netflix_data",
                                                              vectorizer_config=Configure.Vectorizer.text2vec_openai(model="text-embedding-3-small"),
                                                              generative_config=Configure.Generative.openai(model="gpt-4o-mini"))
            with netflix_coll.batch.dynamic() as batch:
                for show in data:
                    batch.add_object(
                        {
                            "title": str(show["text"]["title"]),
                            "director": str(show["text"]["director"]),
                            "description": str(show["text"]["description"]),
                            "type": str(show["metadata"]["type"]),
                            "country": str(show["metadata"]["country"]),
                            "release_year": show["metadata"]["release_year"],
                            "listed_in": str(show["metadata"]["listed_in"]),
                            "duration": str(show["metadata"]["duration"]),
                            "cast": str(show["text"]["cast"])
                        }
                    )
            print("successfully added in docs")
            weaviate_client.close()
        else:
            print("Collection already exists")
    else:
        print("client is not ready")


if __name__ == "__main__":
    filename = "D:/Upwork/Personal_amitdl/Agentic-AI-System/recommendation_engine_agent/agentic-rag-recommendation-engine/sources/netflix_data.xlsx"
    data_list = generate_chunks_and_metadata(filename)
    ingest_data(data_list)
