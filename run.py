import os
from app import create_app

import warnings
warnings.filterwarnings("ignore")

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '80'))
    app.run(debug=True, port=port)