from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionGDriveConfig:
    source_URL: str
    local_data_dir: Path
    local_data_file: Path
    force_ingest: bool

@dataclass(frozen=True)
class PineconeUpsertDocsConfig:
    local_data_file: Path
    load_data_file: Path
    data_length: int
    source_column: str
    metadata_column: list
    openai_api_key: str
    pincone_api_key: str
    pincone_index: str
    namespace: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    document_dimension: str
    id_prefix: str
    force_upsert: bool

@dataclass(frozen=True)
class QnAConfig:
    openai_api_key: str
    pincone_api_key: str
    pincone_index: str
    embedding_model: str
    document_dimension: str
    namespace: str
    llm: str
    temperature: int

@dataclass(frozen=True)
class MemoryConfig:
    openai_api_key: str
    llm: str