import traytable as tt
import pytest

@pytest.fixture
def tray():
	screen = tt.screen(row='PEG', col='protein', maxwell='H6')
	tray = tt.tray(screen, rows=5, cols=6)

	return tray

def test_minimal(tray):
	df = tt.well(tray, 'A3', 'good')

	assert len(df) == 1

def test_log_multiple(tray):
	df = tt.well(tray, ['A3', 'A4'], 'good')

	assert len(df) == 2

def test_append(tray):
	df = tt.well(tray, 'A3', 'good')
	df = tt.well(tray, 'A4', 'bad', old_df=df)

	assert len(df) == 2

def test_maxwell_violation(tray):
	with pytest.raises(ValueError):
		tt.well(tray, 'A7', 'good')

def test_missing_argument(tray):
	with pytest.raises(TypeError):
		tt.well(tray, 'A4')

def main():
	test_invalid_arguments()

if __name__== '__main__': main()
