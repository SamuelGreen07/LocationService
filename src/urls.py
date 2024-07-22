from app import app
from location.urls import location_blueprint
from users.urls import user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(location_blueprint, url_prefix='/location')
