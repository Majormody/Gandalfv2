from ingestion.header_resolver import resolve_headers

def test_single_header():
    data = [
        ["Parameter", "Symbol", "Min", "Max", "Unit"],
        ["Supply Voltage", "VCC", "3.0", "3.6", "V"],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter", "Symbol", "Min", "Max", "Unit"]
    assert vals == [["Supply Voltage", "VCC", "3.0", "3.6", "V"]]


def test_double_header():
    data = [
        ["Parameter", "Symbol", None, None, None],
        [None,        None,     "Min", "Typ", "Max"],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter ", "Symbol ", " Min", " Typ", " Max"]
    assert vals == []


def test_third_case_header():
    data = [
        ["Parameter", "Symbol", None, None, "Unit"],
        ["Supply Voltage", "VCC", "3.0", "3.6", "V"],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter", "Symbol", "", "", "Unit"]
    assert vals == [["Supply Voltage", "VCC", "3.0", "3.6", "V"]]


def test_forth_case_header():
    data = [
        ["Parameter", "Symbol", None, None, None],
        ["Supply Voltage", "VCC", "3.0", "3.6", None],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter", "Symbol", "", "", ""]
    assert vals == [["Supply Voltage", "VCC", "3.0", "3.6", None]]

def test_fifth_case_header():
    data = []
    headers, vals = resolve_headers(data)
    assert headers == []
    assert vals == []

def test_sixth_case_header():
    data = [
        ["Parameter", "Symbol", None, None, None],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter", "Symbol", None, None, None]
    assert vals == []

def test_seventh_case_header():
    data = [
            ["Parameter", "Symbol", None, None, None],
            ["Supply Voltage", "VCC", "3.0", "3.6"],
        ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter Supply Voltage", "Symbol VCC", " 3.0", " 3.6"]
    assert vals == []



def test_eighth_case_header():
    data = [
        ["Parameter", "Symbol","Value", "Value", "Unit"],
        ["Supply Voltage", "VCC", None, "3.6", "V"],
    ]
    headers, vals = resolve_headers(data)
    assert headers == ["Parameter", "Symbol","Value", "Value", "Unit"]
    assert vals == [["Supply Voltage", "VCC", None, "3.6", "V"]]
