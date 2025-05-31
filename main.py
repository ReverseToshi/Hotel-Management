from login import login
from dashboard import Dashboard

is_loggedIn = login()
if is_loggedIn:
    window = Dashboard()