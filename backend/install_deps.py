"""
Simple Installation Helper
==========================

Helper script to install basic dependencies for the FastAPI backend.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using subprocess"""
    try:
        print(f"Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {package}")
            return True
        else:
            print(f"❌ Failed to install {package}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def main():
    """Main installation function"""
    print("🔧 LogViewer Backend Dependency Installer")
    print("=" * 50)
    
    # Essential packages for the backend
    essential_packages = [
        "pydantic==2.5.0",
        "python-dotenv==1.0.0", 
        "aiofiles==23.2.1"
    ]
    
    # FastAPI packages (try to install)
    fastapi_packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "websockets==12.0"
    ]
    
    print("Installing essential packages...")
    for package in essential_packages:
        install_package(package)
    
    print("\nInstalling FastAPI packages...")
    for package in fastapi_packages:
        install_package(package)
    
    print("\n" + "=" * 50)
    print("✅ Installation complete!")
    print("🚀 You can now run the backend test:")
    print("   python test_backend.py")
    print("📡 Or start the full server:")
    print("   python run_server.py")

if __name__ == "__main__":
    main()
