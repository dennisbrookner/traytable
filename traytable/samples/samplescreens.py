import traytable as tt

screen1 = tt.screen('protein', 'PEG', 'H6')
screen1 = tt.tray(screen1, 'tray1', rows=[4,18], cols = [16,21])
screen1 = tt.tray(screen1, 'tray2', rows=[10,17], cols = [15,20])
screen1 = tt.clonetray(screen1, 'tray2', 'tray3', rows = [11,18])

screen2 = tt.screen('protein', 'PEG', 'H6', construct='HEWL',
                    buffer='imidazole', buffermM=20,
                    salt='MnCl2', saltmM=125,
                    PEGMW=400, traytype='MRC48')
screen2 = tt.tray(screen2, 'tray1', rows=[4,18], cols = [16,21],
                  pH=5.4, date='2021-01-01', temp=4)
screen2 = tt.tray(screen2, 'tray2', rows=[10,17], cols = [15,20],
                  pH=5.6, date='2021-01-02', temp=20)
screen2 = tt.clonetray(screen2, 'tray2', 'tray3', rows = [11,18],
                       date='2021-01-04')
