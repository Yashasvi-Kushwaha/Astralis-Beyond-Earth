from services.ingest_service import IngestService

service = IngestService()

result = service.ingest(
    "data/papers/test.pdf"
)

print(result)