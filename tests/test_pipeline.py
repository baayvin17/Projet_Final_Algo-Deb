from app.cleaning.cleaner import clean_data

def test_clean():
    df = clean_data()
    assert df is not None
    assert len(df) > 0