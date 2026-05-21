import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db import add_geo, get_geos

USER_ID = 8110065908

print("Before:", get_geos(USER_ID))
try:
    add_geo(USER_ID, "uy")
    print("Added uy!")
except Exception as e:
    print("Error:", e)
print("After:", get_geos(USER_ID))
