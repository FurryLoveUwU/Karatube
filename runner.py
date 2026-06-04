from app import app
from app.extensions import db


if __name__ == '__main__':
    app.run(debug=True)

    # app.run(host="0.0.0.0", port=5000)