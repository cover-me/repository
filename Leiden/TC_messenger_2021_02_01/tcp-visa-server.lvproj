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
		<Item Name="VIs" Type="Folder">
			<Item Name="ignoreTimeout.vi" Type="VI" URL="../VIs/ignoreTimeout.vi"/>
			<Item Name="processMsg.vi" Type="VI" URL="../VIs/processMsg.vi"/>
			<Item Name="GetTvalue.vi" Type="VI" URL="../VIs/GetTvalue.vi"/>
			<Item Name="GetTCPanel.vi" Type="VI" URL="../VIs/GetTCPanel.vi"/>
			<Item Name="GetTTab.vi" Type="VI" URL="../VIs/GetTTab.vi"/>
			<Item Name="GetRefs.vi" Type="VI" URL="../VIs/GetRefs.vi"/>
			<Item Name="getRef.vi" Type="VI" URL="../VIs/getRef.vi"/>
			<Item Name="GetExeVersion.vi" Type="VI" URL="../VIs/GetExeVersion.vi"/>
		</Item>
		<Item Name="TC_messenger.vi" Type="VI" URL="../TC_messenger.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Internecine Avoider.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/Internecine Avoider.vi"/>
				<Item Name="TCP Listen Internal List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen Internal List.vi"/>
				<Item Name="TCP Listen List Operations.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen List Operations.ctl"/>
				<Item Name="TCP Listen.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
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
				<Property Name="Bld_version.build" Type="Int">16</Property>
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
		</Item>
	</Item>
</Project>
