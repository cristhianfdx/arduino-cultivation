from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import select
from datetime import datetime, timedelta
import time

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'n9tqOMHjlpm4jv2VHI9'
# Api
api = Api(app)
ma = Marshmallow(app)
# Db Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DG7fuOwAk21:PPTMgvGsQ7OXo231lwaZ@localhost:5432/strawberry_cultivation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models


class Sensor(db.Model):

    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=True)
    value = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Sensor %r>' % self.type


class Alert(db.Model):

    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    value = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Alert %r>' % self.description

# Sensor Schema


class SensorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'value', 'created_at')

# Alert Schema


class AlertSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'status', 'value', 'type', 'created_at')


# Init Schemas
sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

alert_schema = AlertSchema()
alerts_schema = AlertSchema(many=True)

# Routes


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


class SensorController(Resource):

    def get(self):
        all_sensors = Sensor.query.all()
        result = sensors_schema.dump(all_sensors)
        return jsonify(list(result))

    def post(self):
        data = request.get_json()
        sensor = None

        for req in data:
            sensor_type = req['type']
            value = float(req['value'])

            if sensor_type == 'hl_sensor':
                sensor = Sensor.query.get(1)
                alert = Alert(type='Humedad Suelo', value=value)

                if value >= 700:
                    alert.description = 'Es necesario iniciar con el riego.'
                    alert.status = 'Informativa'
                    actual_date = datetime.today()
                    min_date = actual_date - timedelta(minutes=20)
                    stmt = select(Alert).where(
                        Alert.created_at.between(min_date, actual_date))
                    alerts = list(db.session.execute(stmt))

                    if len(alerts) < 1:
                        save_alert(alert)

            if sensor_type == 'auto_watering':
                sensor = Sensor.query.get(2)

            if sensor_type == 'relative_humidity':
                sensor = Sensor.query.get(3)
                alert = Alert(type='Humedad Relativa')
                alert.value = '{}%'.format(value)

                if value < 50:
                    alert.description = 'La humedad relativa es baja para condiciones normales.'
                    alert.status = 'Bajo'
                    save_alert(alert)

                if value > 80:
                    alert.description = 'La humedad relativa es alta para condiciones normales.'
                    alert.status = 'Moderado'
                    save_alert(alert)

            if sensor_type == 'temperature':
                sensor = Sensor.query.get(4)
                alert = Alert(type='Temperatura')
                alert.value = '{}°C'.format(value)

                if value < 10:
                    alert.description = 'La temperatura ambiente es muy baja.'
                    alert.status = 'Moderado'
                    save_alert(alert)

                if value > 35:
                    alert.description = 'La temperatura ambiente es muy alta.'
                    alert.status = 'Critico'
                    save_alert(alert)

            if sensor_type == 'heat_index':
                sensor = Sensor.query.get(5)

            sensor.type = sensor_type
            sensor.value = 0 if value == ' NAN' else value
            db.session.commit()
            time.sleep(0.5)

        return {'message': 'Sensor saved successfully'}, 201


class AlertController(Resource):

    def get(self):
        all_alerts = Alert.query.all()
        result = alerts_schema.dump(all_alerts)
        return jsonify(list(result))


def save_alert(alert):
    db.session.add(alert)
    db.session.commit()


api.add_resource(SensorController, '/api/sensors')
api.add_resource(AlertController, '/api/alerts')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
