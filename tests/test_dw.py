from app.db.postgres import insert_dw

def test_dw():
    # test juste que ça crash pas
    insert_dw()
    assert True