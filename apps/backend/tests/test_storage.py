from src.app.storage import get_s3_client


def test_s3_client_init():
    client = get_s3_client()
    assert client is not None
