"""
 Appendis the project root to the system path.
"""
import sys
import os

# Append parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
