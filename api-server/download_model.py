import os
from pathlib import Path
import sys

def download_model_from_gcs():
    """Download model from Google Cloud Storage if not already present."""
    
    model_dir = Path("/app/models/model1")
    model_file = model_dir / "best_model.pt"
    
    # Check if model already exists
    if model_file.exists():
        print(f"✅ Model already downloaded at {model_file}")
        print(f"   Model size: {model_file.stat().st_size / (1024**3):.2f} GB")
        return True
    
    # Create models directory
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Get bucket name from environment
    bucket_name = os.getenv("GCS_BUCKET", "nailhealth-ai-models-nailhealth")
    blob_prefix = "model1/"
    
    print(f"📥 Downloading model from gs://{bucket_name}/{blob_prefix}...")
    print(f"   Target directory: {model_dir}")
    
    try:
        from google.cloud import storage
        
        # Initialize storage client (uses default credentials in Cloud Run)
        print("   Initializing Google Cloud Storage client...")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # List all blobs in the model1/ directory
        blobs = list(bucket.list_blobs(prefix=blob_prefix))
        
        if not blobs:
            print(f"❌ No files found in gs://{bucket_name}/{blob_prefix}")
            return False
        
        print(f"   Found {len(blobs)} files to download...")
        
        # Download each blob
        for blob in blobs:
            # Skip directory markers
            if blob.name.endswith('/'):
                continue
            
            # Skip files in subdirectories (only download files directly in model1/)
            relative_path = blob.name[len(blob_prefix):]
            if '/' in relative_path:
                print(f"   Skipping subdirectory file: {blob.name}")
                continue
            
            # Get relative path and create local file path
            local_file = model_dir / relative_path
            
            # Create parent directories if needed
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Download the file with progress bar
            print(f"   Downloading: {blob.name} → {local_file.name}")
            print(f"   Size: {blob.size / (1024**3):.2f} GB")
            
            # Download with progress tracking
            from tqdm import tqdm
            
            class DownloadProgressBar(tqdm):
                def update_to(self, current, total):
                    self.total = total
                    self.update(current - self.n)
            
            with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc='   Progress') as pbar:
                def progress_callback(bytes_transferred):
                    pbar.update_to(bytes_transferred, blob.size)
                
                # Download file
                with open(str(local_file), 'wb') as f:
                    blob.download_to_file(f)
                    # Update progress to 100%
                    pbar.update_to(blob.size, blob.size)
            
            file_size_mb = local_file.stat().st_size / (1024**2)
            print(f"   ✓ Downloaded: {file_size_mb:.1f} MB")
        
        # Verify the main model file was downloaded
        if model_file.exists():
            file_size_gb = model_file.stat().st_size / (1024**3)
            print(f"\n✅ Model downloaded successfully!")
            print(f"   File: {model_file}")
            print(f"   Size: {file_size_gb:.2f} GB")
            return True
        else:
            print(f"❌ Model file not found after download: {model_file}")
            return False
        
    except ImportError:
        print("❌ google-cloud-storage library not found")
        print("   Install with: pip install google-cloud-storage")
        return False
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = download_model_from_gcs()
    if not success:
        print("\n⚠️  Model download failed!")
        print("   The API will not work without the model.")
        print("   Please check:")
        print("   1. GCS_BUCKET environment variable is correct")
        print("   2. Model exists at gs://[BUCKET]/model1/best_model.pt")
        print("   3. Service account has read permissions")
        sys.exit(1)
    else:
        print("\n🎉 Model ready for inference!")
