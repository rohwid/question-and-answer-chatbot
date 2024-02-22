from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionGDriveConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    unzip_data: str

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