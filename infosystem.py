from infosystem import application

if __name__ == '__main__':
    application.load_app().run(host='localhost', port=5000, debug=True)
