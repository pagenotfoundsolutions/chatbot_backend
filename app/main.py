from app.bootstrap.application_bootstrap import create_app

# main.py is the entry point only — all wiring lives in the bootstrap layer.
app = create_app()
