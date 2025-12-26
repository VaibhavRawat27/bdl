[Setup]
AppName=BDL
AppVersion=1.0.0
DefaultDirName={pf}\BDL
DefaultGroupName=BDL
OutputBaseFilename=BDL-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\bdl.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\BDL"; Filename: "{app}\bdl.exe"

[Registry]
Root: HKCU; Subkey: "Environment"; \
ValueType: expandsz; ValueName: "Path"; \
ValueData: "{olddata};{app}"; \
Check: NeedsAddPath

[Code]
function NeedsAddPath(): Boolean;
var
  Path: string;
begin
  if not RegQueryStringValue(
    HKCU, 'Environment', 'Path', Path) then
    Result := True
  else
    Result := Pos(ExpandConstant('{app}'), Path) = 0;
end;
