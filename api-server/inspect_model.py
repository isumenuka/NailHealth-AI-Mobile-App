"""
Inspect the trained model file to understand its structure and how to load it.
"""
import torch
import sys
from pathlib import Path

model_path = Path(r"c:\Users\Isum Enuka\Downloads\NailHealth-AI-Mobile-App\model 1\best_model.pt")

print(f"Model file: {model_path}")
print(f"Size: {model_path.stat().st_size / (1024**3):.2f} GB\n")

try:
    # Load the model checkpoint
    print("Loading model checkpoint...")
    checkpoint = torch.load(model_path, map_location='cpu')
    
    print(f"\nCheckpoint type: {type(checkpoint)}")
    
    if isinstance(checkpoint, dict):
        print(f"\nCheckpoint keys: {list(checkpoint.keys())}\n")
        
        # Check for common keys
        if 'model_state_dict' in checkpoint:
            print("✓ Found 'model_state_dict'")
            model_state = checkpoint['model_state_dict']
            print(f"  State dict keys (first 10): {list(model_state.keys())[:10]}")
            
        if 'model' in checkpoint:
            print("✓ Found 'model'")
            print(f"  Model type: {type(checkpoint['model'])}")
            
        if 'epoch' in checkpoint:
            print(f"✓ Trained for {checkpoint['epoch']} epochs")
            
        if 'best_val_accuracy' in checkpoint or 'best_accuracy' in checkpoint:
            acc_key = 'best_val_accuracy' if 'best_val_accuracy' in checkpoint else 'best_accuracy'
            print(f"✓ Best accuracy: {checkpoint[acc_key]:.4f}")
            
        if 'config' in checkpoint:
            print(f"✓ Config: {checkpoint['config']}")
            
    else:
        # Model might be saved as the model object directly
        print(f"Model is saved as: {type(checkpoint)}")
        if hasattr(checkpoint, 'state_dict'):
            print("Model has state_dict method")
            
    print("\n" + "="*50)
    print("Model Structure Summary")
    print("="*50)
    
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
