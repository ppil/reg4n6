#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output
import struct
import codecs

guids = {'{7B0DB17D-9CD2-4A93-9733-46CC89022E7C}': '%APPDATA%\Microsoft\Windows\Libraries\Documents.library-ms',
'{DE974D24-D9C6-4D3E-BF91-F4455120B917}': '%ProgramFiles%\CommonFiles',
'{B7534046-3ECB-4C18-BE4E-64CD4CB7D6AC}': 'RecycleBin',
'{8AD10C31-2ADB-4296-A8F7-E4701232C972}': '%windir%\Resources',
'{A4115719-D62E-491D-AA7C-E74B8BE3B067}': '%ALLUSERSPROFILE%\Microsoft\Windows\StartMenu',
'{E555AB60-153B-4D17-9F04-A5FE99FC15EC}': '%ALLUSERSPROFILE%\Microsoft\Windows\Ringtones',
'{B97D20BB-F46A-4C97-BA10-5E3608430854}': '%APPDATA%\Microsoft\Windows\StartMenu\Programs\StartUp',
'{82A5EA35-D9CD-47C5-9629-E15D2F714E6E}': '%ALLUSERSPROFILE%\Microsoft\Windows\StartMenu\Programs\StartUp',
'{7B396E54-9EC5-4300-BE0A-2482EBAE1A26}': '%ProgramFiles%\WindowsSidebar\Gadgets',
'{56784854-C6CB-462B-8169-88E350ACB882}': '%USERPROFILE%\Contacts',
'{A63293E8-664E-48DB-A079-DF759E0509F7}': '%APPDATA%\Microsoft\Windows\Templates',
'{F7F1ED05-9F6D-47A2-AAAE-29D317C6F066}': '%ProgramFiles%\CommonFiles',
'{905E63B6-C1BF-494E-B29C-65B732D3D21A}': '%ProgramFiles%',
'{AE50C081-EBD2-438A-8655-8A092E34987A}': '%APPDATA%\Microsoft\Windows\Recent',
'{190337D1-B8CA-4121-A639-6D472D16972A}': 'SearchResults',
'{4D9F7874-4E0C-4904-967B-40B0D20C3E4B}': 'TheInternet',
'{C4900540-2379-4C75-844B-64E6FAF8716B}': '%PUBLIC%\Pictures\SamplePictures',
'{A305CE99-F527-492B-8B1A-7E76FA98D6E4}': 'InstalledUpdates',
'{2A00375E-224C-49DE-B8D1-440DF7EF3DDC}': '%windir%\resources 9(codepage)',
'{52A4F021-7B75-48A9-9F6B-4B87A210BC8F}': '%APPDATA%\Microsoft\InternetExplorer\QuickLaunch',
'{ED4824AF-DCE4-45A8-81E2-FC7965083634}': '%PUBLIC%\Documents',
'{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}': '%USERPROFILE%\Links',
'{D9DC8A3B-B784-432E-A781-5A1130A75963}': '%LOCALAPPDATA%\Microsoft\Windows\History',
'{2112AB0A-C86A-4FFE-A368-0DE96E47012E}': '%APPDATA%\Microsoft\Windows\Libraries\Music.library-ms',
'{2400183A-6185-49FB-A2D8-4A392A602BA3}': '%PUBLIC%\Videos',
'{352481E8-33BE-4251-BA85-6007CAEDCF9D}': '%LOCALAPPDATA%\Microsoft\Windows\TemporaryInternetFiles',
'{3D644C9B-1FB8-4F30-9B45-F670235F79C0}': '%PUBLIC%\Downloads',
'{33E28130-4E1E-4676-835A-98395C3BC3BB}': '%USERPROFILE%\Pictures',
'{1A6FDBA2-F42D-4358-A798-B74D745926C5}': '%PUBLIC%\RecordedTV.library-ms',
'{1B3EA5DC-B587-4786-B4EF-BD1DC332AEAE}': '%APPDATA%\Microsoft\Windows\Libraries',
'{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}': '%ALLUSERSPROFILE%\Microsoft\Windows\StartMenu\Programs',
'{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}': '%USERPROFILE%\SavedGames',
'{9274BD8D-CFD1-41C3-B35E-B13F55A758F4}': '%APPDATA%\Microsoft\Windows\PrinterShortcuts',
'{A520A1A4-1780-4FF6-BD18-167343C5AF16}': '%USERPROFILE%\AppData\LocalLow',
'{EE32E446-31CA-4ABA-814F-A5EBD2FD6D5E}': 'OfflineFiles',
'{D20BEEC4-5CA8-4905-AE3B-BF251EA09B53}': 'Network',
'{52528A6B-B9E3-4ADD-B60D-588C2DBA842D}': 'Homegroup',
'{5CD7AEE2-2219-4A67-B85D-6C9CE15660CB}': '%LOCALAPPDATA%\Programs',
'{2C36C0AA-5812-4B87-BFD0-4CD0DFB19B39}': '%LOCALAPPDATA%\Microsoft\WindowsPhotoGallery\OriginalImages',
'{6F0CD92B-2E97-45D1-88FF-B0D186B8DEDD}': 'NetworkConnections',
'{D0384E7D-BAC3-4797-8F14-CBA229B392B5}': '%ALLUSERSPROFILE%\Microsoft\Windows\StartMenu\Programs\AdministrativeTools',
'{15CA69B3-30EE-49C1-ACE1-6B5EC372AFB5}': '%PUBLIC%\Music\SamplePlaylists',
'{18989B1D-99B5-455B-841C-AB7C74E4DDFC}': '%USERPROFILE%\Videos',
'{B250C668-F57D-4EE1-A63C-290EE7D1AA1F}': '%PUBLIC%\Music\SampleMusic',
'{BCB5256F-79F6-4CEE-B725-DC34E402FD46}': '%APPDATA%\Microsoft\InternetExplorer\QuickLaunch\UserPinned\ImplicitAppShortcuts',
'{374DE290-123F-4565-9164-39C4925E467B}': '%USERPROFILE%\Downloads',
'{289A9A43-BE44-4057-A41B-587A76D7E7F9}': 'SyncResults',
'{DFDF76A2-C82A-4D63-906A-5644AC457385}': '%PUBLIC%(%SystemDrive%\Users\Public)',
'{48DAF80B-E6CF-4F4E-B800-0E69D84EE384}': '%ALLUSERSPROFILE%\Microsoft\Windows\Libraries',
'{A990AE9F-A03B-4E80-94BC-9912D7504104}': '%APPDATA%\Microsoft\Windows\Libraries\Pictures.library-ms',
'{859EAD94-2E85-48AD-A71A-0969CB56A6CD}': '%PUBLIC%\Videos\SampleVideos',
'{C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}': '%PUBLIC%\Desktop',
'{2B0F765D-C0E9-4171-908E-08A611B84FF6}': '%APPDATA%\Microsoft\Windows\Cookies',
'{491E922F-5643-4AF4-A7EB-4E7A138D8174}': '%APPDATA%\Microsoft\Windows\Libraries\Videos.library-ms',
'{DEBF2536-E1A8-4C59-B6A2-414586476AEA}': '%ALLUSERSPROFILE%\Microsoft\Windows\GameExplorer',
'{0AC0837C-BBF8-452A-850D-79D08E667CA7}': '(My)Computer',
'{0762D272-C50A-4BB0-A382-697DCD729B80}': '%SystemDrive%\Users',
'{69D2CF90-FC33-4FB7-9A0C-EBB0F0FCB43C}': '%USERPROFILE%\Pictures\SlideShows',
'{5E6C858F-0E22-4760-9AFE-EA3317B67173}': '%USERPROFILE%(%SystemDrive%\Users\%USERNAME%)',
'{8983036C-27C0-404B-8F08-102D10DCFD74}': '%APPDATA%\Microsoft\Windows\SendTo',
'{76FC4E2D-D6AD-4519-A663-37BD56068185}': 'Printers',
'{DE61D971-5EBC-4F02-A3A9-6C82895E5C04}': 'AddorRemovePrograms(ControlPanel)',
'{F38BF404-1D43-42F2-9305-67DE0B28FC23}': '%windir%',
'{B94237E7-57AC-4347-9151-B08C6C32D1F7}': '%ALLUSERSPROFILE%\Microsoft\Windows\Templates',
'{625B53C3-AB48-4EC1-BA1F-A1EF4146FC19}': '%APPDATA%\Microsoft\Windows\StartMenu',
'{7D1D3A04-DEBB-4115-95CF-2F29DA2920DA}': '%USERPROFILE%\Searches',
'{6D809377-6AF0-444B-8957-A3773F02200E}': '%ProgramFiles%',
'{724EF170-A42D-4FEF-9F26-B60E846FBA4F}': '%APPDATA%\Microsoft\Windows\StartMenu\Programs\AdministrativeTools',
'{6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D}': '%ProgramFiles%\CommonFiles',
'{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}': '%ALLUSERSPROFILE%(%ProgramData%,%SystemDrive%\ProgramData)',
'{D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}': '%windir%\system32',
'{A75D362E-50FC-4FB7-AC2C-A8BEAA314493}': '%LOCALAPPDATA%\Microsoft\WindowsSidebar\Gadgets',
'{1777F761-68AD-4D8A-87BD-30B759FA33DD}': '%USERPROFILE%\Favorites',
'{B6EBFB86-6907-413C-9AF7-4FC2ABF07CC5}': '%PUBLIC%\Pictures',
'{F3CE0F7C-4901-4ACC-8648-D5D44B04EF8F}': "Theuser'sfullname", '{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}': '%LOCALAPPDATA%(%USERPROFILE%\AppData\Local)',
'{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}': '%APPDATA%(%USERPROFILE%\AppData\Roaming)',
'{4BD8D571-6D19-48D3-BE97-422220080E43}': '%USERPROFILE%\Music',
'{0F214138-B1D3-4A90-BBA9-27CBC0C5389A}': 'SyncSetup',
'{82A74AEB-AEB4-465C-A014-D097EE346D63}': 'ControlPanel',
'{C870044B-F49E-4126-A9C3-B52A1FF411E8}': '%LOCALAPPDATA%\Microsoft\Windows\Ringtones',
'{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}': '%APPDATA%\Microsoft\Windows\StartMenu\Programs',
'{C5ABBF53-E17F-4121-8900-86626FC2C973}': '%APPDATA%\Microsoft\Windows\NetworkShortcuts',
'{C1BAE2D0-10DF-4334-BEDD-7AA20B227A9D}': '%ALLUSERSPROFILE%\OEMLinks',
'{BCBD3057-CA5C-4622-B42D-BC56DB0AE516}': '%LOCALAPPDATA%\Programs\Common',
'{4BFEFB45-347D-4006-A5BE-AC0CB0567192}': 'Conflicts',
'{DE92C1C7-837F-4F69-A3BB-86E631204A23}': '%USERPROFILE%\Music\Playlists',
'{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}': '%ProgramFiles%',
'{3214FAB5-9757-4298-BB61-92A9DEAA44FF}': '%PUBLIC%\Music',
'{98EC0E18-2098-4D44-8644-66979315A281}': 'MicrosoftOfficeOutlook',
'{054FAE61-4DD8-4787-80B6-090220C4B700}': 'GameExplorer',
'{5CE4A5E9-E4EB-479D-B89F-130C02886155}': '%ALLUSERSPROFILE%\Microsoft\Windows\DeviceMetadataStore',
'{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}': 'Desktop',
'{DF7266AC-9274-4867-8D55-3BD661DE872D}': 'ProgramsandFeatures',
'{A302545D-DEFF-464B-ABE8-61C8648D939B}': 'Libraries',
'{FD228CB7-AE11-4AE3-864C-16F3910AB8FE}': '%windir%\Fonts',
'{9E3995AB-1F9C-4F13-B827-48B24B6C7174}': '%APPDATA%\Microsoft\InternetExplorer\QuickLaunch\UserPinned',
'{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}': '%windir%\system32',
'{43668BF8-C14E-49B2-97C9-747784D784B7}': 'SyncCenter',
'{CAC52C1A-B53D-4EDC-92D7-6B2E8AC19434}': 'Games',
'{9E52AB10-F80D-49DF-ACB8-4330F5687855}': '%LOCALAPPDATA%\Microsoft\Windows\Burn\Burn'}

# https://www.aldeid.com/wiki/Windows-userassist-keys
def userassist(cfg, user_hives):
	rows = [["Target", "Run Count", "Focus (ms)", "Last Run"]]
	for username, uhive in user_hives.iteritems():
		for key in common.find_keys_name(common.safe_open(uhive, "Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"), "Count", 2):
			for value in common.safe_open(uhive, key).values():
				vals = {}
				vals["Target"] = codecs.encode(value.name(), 'rot_13').replace('\0','')
				if "UEME_" in vals["Target"]:
					continue
				for guid in guids.keys():
					up = vals["Target"].upper()
					if guid in up:
						vals["Target"] = up.replace(guid, guids[guid])
				data = value.value()
				vals["Run Count"] = struct.unpack("I", data[4:8])[0]
				vals["Focus (ms)"] = struct.unpack("I", data[12:16])[0]
				if struct.unpack("Q", data[60:68])[0]:
					vals["Last Run"] = common.decode_filetime(data[60:68])
				output.dict_to_arr(rows, vals)
		if len(rows) > 1:
			rows = output.sort_by_col(rows, "Target")
			output.write_out(cfg, rows, "Userassist - %s"%username, 1)
