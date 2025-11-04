; Inno Setup Script for SleekCompressor

[Setup]
AppName=SleekCompressor
AppVersion=1.0
AppPublisher=Mehta
DefaultDirName={autopf}\SleekCompressor
DefaultGroupName=SleekCompressor
DisableProgramGroupPage=yes
OutputDir=Release
OutputBaseFilename=SleekCompressor_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; NOTE: The source file is the EXE from your dist folder
Source: "dist\SleekCompressor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SleekCompressor"; Filename: "{app}\SleekCompressor.exe"
Name: "{autodesktop}\SleekCompressor"; Filename: "{app}\SleekCompressor.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\SleekCompressor.exe"; Description: "{cm:LaunchProgram,SleekCompressor}"; Flags: nowait postinstall skipifsilent