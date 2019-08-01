<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="17008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="TC" Type="Folder">
			<Item Name="ignoreTimeout.vi" Type="VI" URL="../TC/ignoreTimeout.vi"/>
			<Item Name="processMsg.vi" Type="VI" URL="../TC/processMsg.vi"/>
			<Item Name="GetTvalue.vi" Type="VI" URL="../TC/GetTvalue.vi"/>
			<Item Name="GetTCPanel.vi" Type="VI" URL="../TC/GetTCPanel.vi"/>
			<Item Name="GetTTab.vi" Type="VI" URL="../TC/GetTTab.vi"/>
		</Item>
		<Item Name="FP" Type="Folder">
			<Item Name="GetConfig.vi" Type="VI" URL="../FP/GetConfig.vi"/>
			<Item Name="GetFPPanel.vi" Type="VI" URL="../FP/GetFPPanel.vi"/>
			<Item Name="GetFPMainPage.vi" Type="VI" URL="../FP/GetFPMainPage.vi"/>
			<Item Name="GetPTInfo.vi" Type="VI" URL="../FP/GetPTInfo.vi"/>
			<Item Name="GetPTError.vi" Type="VI" URL="../FP/GetPTError.vi"/>
		</Item>
		<Item Name="other VIs" Type="Folder">
			<Item Name="increasedNumber.vi" Type="VI" URL="../other VIs/increasedNumber.vi"/>
			<Item Name="SMTPSimple.vi" Type="VI" URL="../other VIs/SMTPSimple.vi"/>
			<Item Name="GetExeVersion.vi" Type="VI" URL="../other VIs/GetExeVersion.vi"/>
			<Item Name="alarmBeep.vi" Type="VI" URL="../other VIs/alarmBeep.vi"/>
			<Item Name="myBeep.vi" Type="VI" URL="../other VIs/myBeep.vi"/>
		</Item>
		<Item Name="TC_messenger.vi" Type="VI" URL="../TC_messenger.vi"/>
		<Item Name="FP_monitor.vi" Type="VI" URL="../FP_monitor.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Beep.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/Beep.vi"/>
				<Item Name="Internecine Avoider.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/Internecine Avoider.vi"/>
				<Item Name="TCP Listen Internal List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen Internal List.vi"/>
				<Item Name="TCP Listen List Operations.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen List Operations.ctl"/>
				<Item Name="TCP Listen.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="NI_LVConfig.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/config.llb/NI_LVConfig.lvlib"/>
				<Item Name="Check if File or Folder Exists.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Check if File or Folder Exists.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="NI_PackedLibraryUtility.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/LVLibp/NI_PackedLibraryUtility.lvlib"/>
				<Item Name="8.6CompatibleGlobalVar.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/config.llb/8.6CompatibleGlobalVar.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
			</Item>
			<Item Name="System" Type="VI" URL="System">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="TC_messenger" Type="EXE">
				<Property Name="App_INI_aliasGUID" Type="Str">{8415817D-3487-4AF5-8231-D28618B8DCF1}</Property>
				<Property Name="App_INI_GUID" Type="Str">{A1D73974-95CE-4BA5-968F-64C011808771}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{68FF0D7A-8EAB-4DC8-B4AE-A27F9518E0AB}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">TC_messenger</Property>
				<Property Name="Bld_defaultLanguage" Type="Str">ChineseS</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/TC_messenger</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{292EC531-F14B-46AC-A38D-2C1C7824112A}</Property>
				<Property Name="Bld_targetDestDir" Type="Path"></Property>
				<Property Name="Bld_version.build" Type="Int">15</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">TC_messenger.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/TC_messenger/TC_messenger.exe</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">????</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/TC_messenger/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_actXinfo_enumCLSID[0]" Type="Str">{9E5F9025-BB5F-4C16-AB27-F90F6591D424}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[1]" Type="Str">{E445C56C-D283-46F6-9E1D-3A970CAD372E}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[10]" Type="Str">{D1FBA252-E794-4693-B1C6-9B2F6E0091D7}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[11]" Type="Str">{7FC2CCD4-8DE1-433D-8667-F7894D0E0ED6}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[12]" Type="Str">{572C5D0D-69BE-45E8-9C44-FEF6C6046BA4}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[13]" Type="Str">{A79A8A65-1EE2-4998-BB31-D3B01DE2A1C9}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[14]" Type="Str">{C934D2BB-C63B-45BE-B93E-DB9AF04064E0}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[15]" Type="Str">{2D323995-E833-412E-94AD-BB07FC406B16}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[16]" Type="Str">{4E28D1DC-532C-413D-A1AF-3AA5BB3704E6}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[2]" Type="Str">{1224D7BE-8CC1-439B-A33B-9DC8376AEC98}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[3]" Type="Str">{40DF601B-DC68-4F99-9165-52A60115DDD1}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[4]" Type="Str">{71EFCBD0-99F8-412B-BCE1-1DFAD557BD9E}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[5]" Type="Str">{C5E4CA1E-DE6B-47CC-9C98-F658F4322CD1}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[6]" Type="Str">{6AEF85ED-2E08-4B29-80C6-60AE4CD87680}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[7]" Type="Str">{BFADC0F6-8684-437D-95E4-C159CD233C68}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[8]" Type="Str">{7784388D-11C6-4C0E-9526-A0A81B46F163}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[9]" Type="Str">{E68A42EC-407C-4351-8A33-BBB751A92687}</Property>
				<Property Name="Exe_actXinfo_enumCLSIDsCount" Type="Int">17</Property>
				<Property Name="Exe_actXinfo_majorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_minorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_objCLSID[0]" Type="Str">{5D85A915-85EE-4DE3-9105-95CAF5D8B557}</Property>
				<Property Name="Exe_actXinfo_objCLSID[1]" Type="Str">{6D3C8527-3CA5-4E87-BE73-00F2974EE930}</Property>
				<Property Name="Exe_actXinfo_objCLSID[2]" Type="Str">{75E4EB88-234A-4E54-8231-989B702B32E7}</Property>
				<Property Name="Exe_actXinfo_objCLSID[3]" Type="Str">{4FCBBB9C-C64F-49A6-B9A1-A9B275DFC043}</Property>
				<Property Name="Exe_actXinfo_objCLSID[4]" Type="Str">{47602447-7929-4F65-9206-EC585E3F25AD}</Property>
				<Property Name="Exe_actXinfo_objCLSID[5]" Type="Str">{8B00495F-9654-4AC5-8366-F86D35EAE7BA}</Property>
				<Property Name="Exe_actXinfo_objCLSIDsCount" Type="Int">6</Property>
				<Property Name="Exe_actXinfo_progIDPrefix" Type="Str">AVSWrap</Property>
				<Property Name="Exe_actXServerName" Type="Str">TCMessenger</Property>
				<Property Name="Exe_actXServerNameGUID" Type="Str">{4AAC2E7E-DF5A-4186-8453-32463A3F79A9}</Property>
				<Property Name="Source[0].itemID" Type="Str">{37AB2016-BFA4-4936-8A3D-F08B76980306}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/TC_messenger.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fileDescription" Type="Str">TC_messenger</Property>
				<Property Name="TgtF_internalName" Type="Str">TC_messenger</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">?? 2018 </Property>
				<Property Name="TgtF_productName" Type="Str">TC_messenger</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{E8EABD4A-82E9-4C8F-8679-1934684F719A}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">TC_messenger.exe</Property>
			</Item>
			<Item Name="FP_monitor" Type="EXE">
				<Property Name="App_INI_aliasGUID" Type="Str">{55E1C964-CFD5-4D20-9F35-51682F21543E}</Property>
				<Property Name="App_INI_GUID" Type="Str">{425FA2F7-5536-430B-8ED7-E915C6DF0CC4}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{15BE4D9E-ED53-4C5F-825C-EFCA9473CD0A}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">FP_monitor</Property>
				<Property Name="Bld_defaultLanguage" Type="Str">ChineseS</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/NI_AB_PROJECTNAME/FP_monitor</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{8F1A637F-065F-4928-82CA-36952DE83C36}</Property>
				<Property Name="Bld_targetDestDir" Type="Path"></Property>
				<Property Name="Bld_version.build" Type="Int">8</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">FP_monitor.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/FP_monitor/FP_monitor.exe</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">????</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/FP_monitor/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_actXinfo_enumCLSID[0]" Type="Str">{D3D4194C-E4A8-4081-817E-F5254245F6AE}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[1]" Type="Str">{7514B46F-2693-4C39-8F6B-16A27013B7FF}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[10]" Type="Str">{83DF35FB-CFE6-49A7-8126-A9DEAA0A3F75}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[11]" Type="Str">{2E6489E3-F3ED-45DB-95FD-6C2E6F1734F6}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[12]" Type="Str">{275AACB8-A413-44E5-BC37-DBFC70EBF394}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[13]" Type="Str">{35682FAC-DD5A-423E-AB5B-B64F9B163017}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[14]" Type="Str">{EDEE922B-77FD-4AB3-8F6D-5C09A0EB71F2}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[15]" Type="Str">{9D655151-A937-493D-88EB-95B7E3687E8F}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[16]" Type="Str">{39B8CB1A-1BFC-4A34-BB76-AF6C58043D08}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[2]" Type="Str">{052930E9-BE36-4FEA-A588-E9C7C408887E}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[3]" Type="Str">{9B605F89-23B1-451C-8DDD-E6436FA23241}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[4]" Type="Str">{93F70CC6-7F84-408D-8550-9B109B47ED0E}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[5]" Type="Str">{57FCA9DC-EFB9-46A5-8209-D0B05F00F935}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[6]" Type="Str">{F8EC32ED-51A8-4E7B-B5C5-B73757F6B383}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[7]" Type="Str">{70DB3C73-4431-479B-BD31-21C55FAD5AB5}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[8]" Type="Str">{593AF8BE-AB59-4E23-9619-9075D4BFE281}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[9]" Type="Str">{66788543-8816-4DBE-92B2-CA84B89DA0B5}</Property>
				<Property Name="Exe_actXinfo_enumCLSIDsCount" Type="Int">17</Property>
				<Property Name="Exe_actXinfo_majorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_minorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_objCLSID[0]" Type="Str">{F311BD7C-EC08-41F5-BCB5-20B9B8EF8D24}</Property>
				<Property Name="Exe_actXinfo_objCLSID[1]" Type="Str">{3D95CC29-51C6-4D29-A325-5B66E915CA1E}</Property>
				<Property Name="Exe_actXinfo_objCLSID[2]" Type="Str">{CDB9C038-33B0-4247-B6F4-C9ACFDDCF5D8}</Property>
				<Property Name="Exe_actXinfo_objCLSID[3]" Type="Str">{EC11A3A3-7044-4C79-85FD-996009A25CCB}</Property>
				<Property Name="Exe_actXinfo_objCLSID[4]" Type="Str">{173B9662-AA34-4361-BACE-ACCE1BEC8932}</Property>
				<Property Name="Exe_actXinfo_objCLSID[5]" Type="Str">{D031F2D5-924D-489A-8FD6-1FF39C9F5965}</Property>
				<Property Name="Exe_actXinfo_objCLSIDsCount" Type="Int">6</Property>
				<Property Name="Exe_actXinfo_progIDPrefix" Type="Str">FPMonitor</Property>
				<Property Name="Exe_actXServerName" Type="Str">FPMonitor</Property>
				<Property Name="Exe_actXServerNameGUID" Type="Str">{0A83E9FA-17A5-4CE6-8B36-B8F92F6C8BE2}</Property>
				<Property Name="Source[0].itemID" Type="Str">{67C1D994-C86A-4DA0-847B-6164D20CFC95}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/FP_monitor.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_fileDescription" Type="Str">FP_monitor</Property>
				<Property Name="TgtF_internalName" Type="Str">FP_monitor</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">?? 2018 </Property>
				<Property Name="TgtF_productName" Type="Str">FP_monitor</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{C7BD084B-4C76-4E8B-90D5-46A9DC836990}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">FP_monitor.exe</Property>
			</Item>
		</Item>
	</Item>
</Project>
