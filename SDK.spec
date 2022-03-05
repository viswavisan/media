# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['SDK.py'],
             pathex=[],
             binaries=[],
             datas=[('D:/media/stored/3d.png', 'stored'), ('D:/media/stored/actor.png', 'stored'), ('D:/media/stored/alexa.gif', 'stored'), ('D:/media/stored/ask.png', 'stored'), ('D:/media/stored/back.png', 'stored'), ('D:/media/stored/bg.jpg', 'stored'), ('D:/media/stored/bin.png', 'stored'), ('D:/media/stored/browse.png', 'stored'), ('D:/media/stored/browser.gif', 'stored'), ('D:/media/stored/brush.png', 'stored'), ('D:/media/stored/calculator.gif', 'stored'), ('D:/media/stored/calender.gif', 'stored'), ('D:/media/stored/camera.gif', 'stored'), ('D:/media/stored/camera.png', 'stored'), ('D:/media/stored/capture.png', 'stored'), ('D:/media/stored/cell.png', 'stored'), ('D:/media/stored/clear.png', 'stored'), ('D:/media/stored/color.png', 'stored'), ('D:/media/stored/colorEdit.png', 'stored'), ('D:/media/stored/control.gif', 'stored'), ('D:/media/stored/correct.png', 'stored'), ('D:/media/stored/create.png', 'stored'), ('D:/media/stored/crop.png', 'stored'), ('D:/media/stored/csv.png', 'stored'), ('D:/media/stored/edit.png', 'stored'), ('D:/media/stored/email.png', 'stored'), ('D:/media/stored/excel.gif', 'stored'), ('D:/media/stored/exportxl.png', 'stored'), ('D:/media/stored/filter.png', 'stored'), ('D:/media/stored/find.png', 'stored'), ('D:/media/stored/fit.png', 'stored'), ('D:/media/stored/flip.png', 'stored'), ('D:/media/stored/ford.png', 'stored'), ('D:/media/stored/front.png', 'stored'), ('D:/media/stored/goto.png', 'stored'), ('D:/media/stored/graph.png', 'stored'), ('D:/media/stored/group.png', 'stored'), ('D:/media/stored/groups.ico', 'stored'), ('D:/media/stored/H.png', 'stored'), ('D:/media/stored/help.png', 'stored'), ('D:/media/stored/hide.png', 'stored'), ('D:/media/stored/home.png', 'stored'), ('D:/media/stored/input.gif', 'stored'), ('D:/media/stored/insert.png', 'stored'), ('D:/media/stored/invert.png', 'stored'), ('D:/media/stored/isometric.png', 'stored'), ('D:/media/stored/load.png', 'stored'), ('D:/media/stored/locate.png', 'stored'), ('D:/media/stored/marker.png', 'stored'), ('D:/media/stored/measure.png', 'stored'), ('D:/media/stored/mesh.png', 'stored'), ('D:/media/stored/minus.png', 'stored'), ('D:/media/stored/new.png', 'stored'), ('D:/media/stored/next.png', 'stored'), ('D:/media/stored/open.png', 'stored'), ('D:/media/stored/output.png', 'stored'), ('D:/media/stored/pause.png', 'stored'), ('D:/media/stored/plus.png', 'stored'), ('D:/media/stored/point.png', 'stored'), ('D:/media/stored/previous.png', 'stored'), ('D:/media/stored/progress.png', 'stored'), ('D:/media/stored/prop.png', 'stored'), ('D:/media/stored/python.png', 'stored'), ('D:/media/stored/recenter.png', 'stored'), ('D:/media/stored/record.png', 'stored'), ('D:/media/stored/reject.png', 'stored'), ('D:/media/stored/reload.png', 'stored'), ('D:/media/stored/replace.png', 'stored'), ('D:/media/stored/resize.png', 'stored'), ('D:/media/stored/run.png', 'stored'), ('D:/media/stored/save.PNG', 'stored'), ('D:/media/stored/screen.gif', 'stored'), ('D:/media/stored/screenshot.png', 'stored'), ('D:/media/stored/script.gif', 'stored'), ('D:/media/stored/select.png', 'stored'), ('D:/media/stored/setting.gif', 'stored'), ('D:/media/stored/setting.png', 'stored'), ('D:/media/stored/setting2.gif', 'stored'), ('D:/media/stored/setting3.gif', 'stored'), ('D:/media/stored/show.png', 'stored'), ('D:/media/stored/showall.png', 'stored'), ('D:/media/stored/showonly.png', 'stored'), ('D:/media/stored/snap.png', 'stored'), ('D:/media/stored/stop.png', 'stored'), ('D:/media/stored/stt.png', 'stored'), ('D:/media/stored/submit.png', 'stored'), ('D:/media/stored/T.png', 'stored'), ('D:/media/stored/upload.png', 'stored'), ('D:/media/stored/upload1.png', 'stored'), ('D:/media/stored/vcamera.png', 'stored'), ('D:/media/stored/voice.gif', 'stored'), ('D:/media/stored/voice.png', 'stored'), ('D:/media/stored/vtk.gif', 'stored'), ('D:/media/stored/wrong.png', 'stored')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='SDK',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
