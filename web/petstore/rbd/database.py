# rbd/database.py
import json
import hashlib
import time
from datetime import datetime
import numpy as np
from typing import List, Dict, Any
from .model_loader import get_embedding_model
from .utils import format_record, sort_records

class ReferenceBaseDB:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.store = {}
        self.fingerprints = {}
        self.load()

    def _hash(self, content: str) -> str:
        return "sha3:" + hashlib.sha3_256(content.encode()).hexdigest()[:16]

    def _encode_data(self, data) -> str:
        if isinstance(data, str):
            return f"t:u:{data}"
        elif isinstance(data, (int, float)):
            return f"n:f:{data}"
        elif isinstance(data, list):
            vec_str = ",".join(f"{x:.6f}" for x in data)
            return f"v:f:{vec_str}"
        elif isinstance(data, dict):
            json_str = json.dumps(data, sort_keys=True)
            return f"j:j:{json_str}"
        else:
            return f"u:u:{str(data)}"

    def _decode_data(self, s: str):
        if s.startswith("t:u:"):
            return s[4:]
        elif s.startswith("n:f:"):
            try:
                return float(s[4:])
            except ValueError:
                return s[4:]
        elif s.startswith("v:f:"):
            return [float(x) for x in s[4:].split(",")]
        elif s.startswith("j:j:"):
            return json.loads(s[4:])
        else:
            return s[5:]

    def _vector_to_fingerprint(self, vec: List[float]) -> str:
        rounded = [f"{x:.4f}" for x in vec]
        vec_str = ",".join(rounded)
        return self._hash(f"vf:{vec_str}")

    def load(self):
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self.store = data['store']
                self.fingerprints = data['fingerprints']
        except FileNotFoundError:
            self.store = {}
            self.fingerprints = {}

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump({
                "store": self.store,
                "fingerprints": self.fingerprints
            }, f, indent=2)

    def add(self, data, text_hint: str = None, prev: str = None) -> str:
        encoded_data = self._encode_data(data)
        record = {
            "data": encoded_data,
            "prev": prev,
            "ts": int(time.time()),
            "type": encoded_data.split(":")[0]
        }
        serialized = json.dumps(record, sort_keys=True)
        ref_hash = self._hash(serialized)
        
        # Semantic fingerprint
        if isinstance(data, str) or text_hint:
            text = text_hint or str(data)
            vec = self._text_to_vector(text)
            vf_hash = self._vector_to_fingerprint(vec)
            self.fingerprints.setdefault(vf_hash, []).append(ref_hash)

        self.store[ref_hash] = record
        self.save()
        return ref_hash

    def _text_to_vector(self, text: str) -> List[float]:
        model = get_embedding_model()
        result = model.create_embedding(text)
        return result["data"][0]["embedding"]

    def query_similar(self, text: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        query_vec = self._text_to_vector(text)
        query_vec_np = np.array(query_vec)
        results = []

        for vf_hash, ref_hashes in self.fingerprints.items():
            sample_ref = self.store[ref_hashes[0]]
            decoded = self._decode_data(sample_ref["data"])
            if isinstance(decoded, str):
                stored_vec = self._text_to_vector(decoded)
                stored_vec_np = np.array(stored_vec)
                dot_product = np.dot(query_vec_np, stored_vec_np)
                norm_a = np.linalg.norm(query_vec_np)
                norm_b = np.linalg.norm(stored_vec_np)
                similarity = dot_product / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

                if similarity >= threshold:
                    for ref_hash in ref_hashes:
                        results.append({
                            "ref": ref_hash,
                            "similarity": float(similarity),
                            "data": self._decode_data(self.store[ref_hash]["data"])
                        })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def get_chain(self, start_ref: str) -> List[Any]:
        chain = []
        current_ref = start_ref
        while current_ref and current_ref in self.store:
            record = self.store[current_ref]
            chain.append(self._decode_data(record["data"]))
            current_ref = record["prev"]
        return chain

    def get_all_records(self, sort_by: str = "timestamp", reverse: bool = True) -> List[Dict]:
        """
        Retrieve all records from the database.
        
        Args:
            sort_by: Field to sort by (default: "timestamp")
            reverse: Whether to sort in descending order (newest first)
        
        Returns:
            List of all records with decoded data
        """
        records = []
        
        for ref_hash, record in self.store.items():
            decoded_data = self._decode_data(record["data"])
            formatted_record = format_record(ref_hash, record, decoded_data)
            records.append(formatted_record)
        
        # Sort records using utility function
        return sort_records(records, sort_by, reverse)
    
    def get_records_by_type(self, record_type: str, sort_by: str = "timestamp", reverse: bool = True) -> List[Dict]:
        """
        Retrieve all records of a specific type from the database.
        
        Args:
            record_type: Type of records to retrieve
            sort_by: Field to sort by (default: "timestamp")
            reverse: Whether to sort in descending order (newest first)
        
        Returns:
            List of records with the specified type
        """
        records = []
        
        for ref_hash, record in self.store.items():
            if record.get("type") == record_type:
                decoded_data = self._decode_data(record["data"])
                formatted_record = format_record(ref_hash, record, decoded_data)
                records.append(formatted_record)
        
        # Sort records using utility function
        return sort_records(records, sort_by, reverse)