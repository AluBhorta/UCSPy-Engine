
from server import app, socketio, cleanup

if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0", port=1234)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        cleanup()
