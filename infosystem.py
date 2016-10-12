from infosystem import system


if __name__ == '__main__':
    system = system.System()
    system.run(host='localhost', port=5000, debug=True)
