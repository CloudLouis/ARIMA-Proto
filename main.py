
import arima

from flask import Flask, render_template, request

def worker():
    # read json + reply
    data = request.get_json(force=True)

    prediction = arima.do_prediction(str(data['symbol']))

    return prediction


def create_app(test_config=None):

    app = Flask(__name__)

    @app.route('/')
    def run_app():
        return render_template('index.html')

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()



