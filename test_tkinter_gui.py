#!/usr/bin/env python3
"""
🔥 Test Tkinter Dashboard
Simple test for the tkinter GUI
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_gui.tkinter_dashboard import PhoenixTkinterDashboard

def main():
    """Test tkinter dashboard"""
    print("🔥 Testing Tkinter Dashboard...")
    print("=" * 50)
    
    try:
        # Create dashboard
        dashboard = PhoenixTkinterDashboard()
        
        # Create and show GUI
        root = dashboard.create_gui()
        dashboard.start_update_loop()
        
        # Add test messages
        dashboard.log_message("🔥 Tkinter dashboard test started")
        dashboard.log_message("✅ GUI components loaded successfully")
        dashboard.log_message("📊 Ready for trading system integration")
        
        print("✅ Tkinter GUI started successfully!")
        print("📊 Dashboard window should be visible")
        print("🔄 Close the window to exit")
        
        # Run GUI
        root.mainloop()
        
        print("✅ Tkinter GUI test completed")
        
    except Exception as e:
        print(f"❌ Tkinter GUI test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
