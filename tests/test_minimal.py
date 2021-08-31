import traytable as tt
import pytest

@pytest.mark.xfail
def test_invalid_arguments():
	screen = tt.screen(row='PEG', col='protein', maxwell='H6')
	tray = tt.tray(screen, rows=5, cols=6)
	df = tt.well(tray, 'A7', 'good')

def test_minimal():
	screen = tt.screen(row='PEG', col='protein', maxwell='H6')
	tray = tt.tray(screen, rows=5, cols=6)
	df = tt.well(tray, 'A3', 'good')
