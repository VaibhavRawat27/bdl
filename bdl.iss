[Setup]
AppName=BDL
AppVersion=1.0.0
AppPublisher=BDL Foundation
DefaultDirName={pf}\BDL
DefaultGroupName=BDL
OutputBaseFilename=BDL-Setup
OutputDir=output
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
Source: "dist\bdl.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "examples\*"; DestDir: "{app}\examples"; Flags: recursesubdirs

[Icons]
Name: "{group}\BDL CLI"; Filename: "{app}\bdl.exe"

[Registry]
; Add BDL to PATH
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
ValueType: expandsz; ValueName: "Path"; \
ValueData: "{olddata};{app}"

[Run]
Filename: "{app}\bdl.exe"; Parameters: "version"; Flags: nowait postinstall skipifsilent
