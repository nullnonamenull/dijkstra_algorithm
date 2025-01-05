from src.utils.data_loader import load_csv


def test_load_csv(tmp_path):
    csv_content = "city,lat,lng,country\nWarsaw,52.2297,21.0122,Poland\n"
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    df = load_csv(str(test_file))
    assert len(df) == 1
    assert df.loc[0, "city"] == "Warsaw"
    assert df.loc[0, "country"] == "Poland"
