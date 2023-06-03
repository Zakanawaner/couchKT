from flask import Flask
from utils import createApp, createDatabase

from bpGeneric import genericBP
from bpAuth import authBP
from bpAdmin import adminBP
from bpPackage import packageBP
from bpBlog import blogBP

app = Flask(__name__)
app.register_blueprint(genericBP)
app.register_blueprint(authBP)
app.register_blueprint(adminBP)
app.register_blueprint(packageBP)
app.register_blueprint(blogBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])

# TODO
#  - Definir como se contacta a través del formulario y añadir el package deseado
#  - Blog de entradas a los diferentes contenidos
#  - eliminar manualmente ofertas
#  - Crear Blogs.html
