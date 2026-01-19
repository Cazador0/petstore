# rbd/model_loader.py
import logging
from pathlib import Path
from llama_cpp import Llama

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global model instance
_model = None

def get_embedding_model():
    global _model
    
    # If model already loaded, return it
    if _model is not None:
        logger.debug("Model already loaded, returning cached instance")
        return _model
    
    logger.info("=== Starting Model Loading Process ===")
    
    # Get the directory of the current file
    current_file = Path(__file__).resolve()
    logger.debug(f"Current file location: {current_file}")
    
    # Get the project root directory (parent of rbd folder)
    project_root = current_file.parent.parent
    logger.debug(f"Project root directory: {project_root}")
    
    # Construct model path
    model_path = project_root / "llama.cpp" / "models" / "nomic-embed-text-v1.5.Q5_K_M.gguf"
    logger.debug(f"Constructed model path: {model_path}")
    
    # Check if path exists
    logger.debug(f"Model path exists: {model_path.exists()}")
    logger.debug(f"Model path is file: {model_path.is_file()}")
    
    # List contents of parent directories for debugging
    models_dir = project_root / "llama.cpp" / "models"
    if models_dir.exists():
        logger.debug(f"Contents of models directory: {list(models_dir.iterdir())}")
    
    codellama_dir = models_dir / "CodeLlama-7B-Instruct-GGUF"
    if codellama_dir.exists():
        logger.debug(f"Contents of CodeLlama directory: {list(codellama_dir.iterdir())}")
    
    # Check if model file exists
    if not model_path.exists():
        error_msg = f"""
        ❌ Model file not found!
        Looking for: {model_path}
        Current working directory: {Path.cwd()}
        Project root: {project_root}
        Model directory exists: {model_path.parent.exists()}
        """
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    logger.info(f"✅ Model found at: {model_path}")
    logger.info("🔄 Initializing Llama model (this may take a moment)...")
    
    try:
        # Initialize the model
        _model = Llama(
            model_path=str(model_path),
            embedding=True,
            verbose=True,  # Set to True to see more loading info
            n_ctx=2048,
        )
        logger.info("✅ Model loaded successfully!")
        return _model
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise