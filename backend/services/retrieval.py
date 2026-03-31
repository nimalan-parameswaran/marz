from backend.db.chroma import get_visit_collection
from backend.services.embeddings import embed_text


def save_visit_to_memory(visit_id: str, patient_name: str, visit_text: str, diagnosis: str):
    collection = get_visit_collection()
    embedding = embed_text(visit_text)

    collection.add(
        ids=[visit_id],
        embeddings=[embedding],
        documents=[visit_text],
        metadatas=[{
            "patient_name": patient_name,
            "diagnosis": diagnosis
        }]
    )


def retrieve_similar_visits(current_visit_text: str, patient_name: str, n_results: int = 3) -> list:
    collection = get_visit_collection()

    if collection.count() == 0:
        return []

    embedding = embed_text(current_visit_text)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n_results, collection.count()),
        where={"patient_name": patient_name}
    )

    visits = []
    for i, doc in enumerate(results["documents"][0]):
        visits.append({
            "past_visit": doc,
            "diagnosis": results["metadatas"][0][i]["diagnosis"]
        })

    return visits