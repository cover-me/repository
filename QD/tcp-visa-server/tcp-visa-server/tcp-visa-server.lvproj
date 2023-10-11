<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="8608001">
	<Item Name="My Computer" Type="My Computer">
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
			<Item Name="myBeep.vi" Type="VI" URL="../VIs/myBeep.vi"/>
			<Item Name="processMsg.vi" Type="VI" URL="../VIs/processMsg.vi"/>
		</Item>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="test read temperature.vi" Type="VI" URL="../test read temperature.vi"/>
		<Item Name="test set field read field.vi" Type="VI" URL="../test set field read field.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Beep.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/Beep.vi"/>
				<Item Name="Internecine Avoider.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/Internecine Avoider.vi"/>
				<Item Name="TCP Listen Internal List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen Internal List.vi"/>
				<Item Name="TCP Listen List Operations.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen List Operations.ctl"/>
				<Item Name="TCP Listen.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/tcp.llb/TCP Listen.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
			</Item>
			<Item Name="SetTemperature.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/SetTemperature.vi"/>
			<Item Name="QDInstrumentExceptionHandler.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/QDInstrumentExceptionHandler.vi"/>
			<Item Name="GetTemperature.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/GetTemperature.vi"/>
			<Item Name="OpenQDInstrument.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/OpenQDInstrument.vi"/>
			<Item Name="GetField.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/GetField.vi"/>
			<Item Name="SetField.vi" Type="VI" URL="../PPMS driver/QDInstrument.llb/SetField.vi"/>
			<Item Name="QDInstrument.dll" Type="Document" URL="/G/tcp-visa-server/PPMS driver/QDInstrument.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="tcp-visa-server" Type="EXE">
				<Property Name="App_applicationGUID" Type="Str">{F5D60A1F-1355-4CDC-A781-520D00E77F1B}</Property>
				<Property Name="App_applicationName" Type="Str">tcp-visa-server.exe</Property>
				<Property Name="App_autoIncrement" Type="Bool">true</Property>
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_fileDescription" Type="Str">tcp-visa-server</Property>
				<Property Name="App_fileVersion.build" Type="Int">3</Property>
				<Property Name="App_fileVersion.major" Type="Int">1</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{2057BAA5-25A1-4F54-8AFA-C3729E4A3396}</Property>
				<Property Name="App_INI_GUID" Type="Str">{36C7E116-471F-4049-9894-3C0DC8EC2C46}</Property>
				<Property Name="App_internalName" Type="Str">tcp-visa-server</Property>
				<Property Name="App_legalCopyright" Type="Str">Copyright ?2016 </Property>
				<Property Name="App_productName" Type="Str">tcp-visa-server</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_buildSpecName" Type="Str">tcp-visa-server</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Destination[0].destName" Type="Str">tcp-visa-server.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/tcp-visa-server/internal.llb</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/tcp-visa-server/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{3FDB8ECF-F36F-4D4D-9E10-B530104198FD}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/main.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
			</Item>
			<Item Name="test read temperature" Type="EXE">
				<Property Name="App_applicationGUID" Type="Str">{97A11061-3B06-42BF-81F6-F358C5048179}</Property>
				<Property Name="App_applicationName" Type="Str">test read temperature.exe</Property>
				<Property Name="App_fileDescription" Type="Str">test read temperature</Property>
				<Property Name="App_fileVersion.major" Type="Int">1</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{4F49529E-47D7-4459-B56E-F420CE554515}</Property>
				<Property Name="App_INI_GUID" Type="Str">{BFDEA4DB-6903-4751-A347-95E420B4A3A5}</Property>
				<Property Name="App_internalName" Type="Str">test read temperature</Property>
				<Property Name="App_legalCopyright" Type="Str">版权 2023 </Property>
				<Property Name="App_productName" Type="Str">test read temperature</Property>
				<Property Name="Bld_buildSpecName" Type="Str">test read temperature</Property>
				<Property Name="Bld_defaultLanguage" Type="Str">ChineseS</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Destination[0].destName" Type="Str">test read temperature.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME/test read temperature/internal.llb</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">支持目录</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/NI_AB_PROJECTNAME/test read temperature/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_actXinfo_enumCLSID[0]" Type="Str">{D0074BC5-1C3A-4E3B-9A71-64AB823937C7}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[1]" Type="Str">{28C0602E-B20B-4476-8520-0BE0EA50C97B}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[10]" Type="Str">{7ABFF2BD-5029-4E43-8CFD-5FBC2264AC2D}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[11]" Type="Str">{C3AF294D-D965-4F41-AFC0-F923D8F614F7}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[12]" Type="Str">{35425C42-7F40-418F-BFC0-50364621FE7F}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[13]" Type="Str">{F6355A34-95EC-4705-AF19-EEDD7AEF9020}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[14]" Type="Str">{E144AF6D-2169-48AF-A544-1421FEBBFBA8}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[15]" Type="Str">{A9ACEAD5-2362-447C-9814-277E23EF2A48}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[16]" Type="Str">{930A51CD-D561-4699-8EEC-DBA9F64A944D}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[2]" Type="Str">{659EB2D8-E6BB-403D-91FD-05691650737F}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[3]" Type="Str">{D221E13B-DF26-46FA-AD61-5D0E62A14C57}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[4]" Type="Str">{FCAACCDF-28D4-4120-8E11-BBFCED60B9AC}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[5]" Type="Str">{80D3582B-42E7-4F80-8BEB-5F475473C5FC}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[6]" Type="Str">{86086373-2F0B-49F8-B152-B2879330EE54}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[7]" Type="Str">{9EBA46E2-08D9-464B-9732-039B0B334B38}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[8]" Type="Str">{3A7A94A5-107F-477F-AD1E-0DFA819E5828}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[9]" Type="Str">{0138A44F-B15B-4F24-870C-78DF4D76BC12}</Property>
				<Property Name="Exe_actXinfo_enumCLSIDsCount" Type="Int">17</Property>
				<Property Name="Exe_actXinfo_majorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_minorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_objCLSID[0]" Type="Str">{309DE3D5-CF88-438E-9146-420524870827}</Property>
				<Property Name="Exe_actXinfo_objCLSID[1]" Type="Str">{0DBA15F6-908C-4ED0-B4E6-9E016CE6B351}</Property>
				<Property Name="Exe_actXinfo_objCLSID[2]" Type="Str">{3FDD1424-26F3-4F30-AD4A-62A2E6422F9B}</Property>
				<Property Name="Exe_actXinfo_objCLSID[3]" Type="Str">{372809D2-3136-4796-8A0E-B146A7BD49EF}</Property>
				<Property Name="Exe_actXinfo_objCLSID[4]" Type="Str">{60A51D15-BD59-498C-B301-3F4569741CDD}</Property>
				<Property Name="Exe_actXinfo_objCLSID[5]" Type="Str">{9314D3BA-1D4E-457E-985C-1CCF38F4D1CE}</Property>
				<Property Name="Exe_actXinfo_objCLSIDsCount" Type="Int">6</Property>
				<Property Name="Exe_actXinfo_progIDPrefix" Type="Str">TestReadTemperature</Property>
				<Property Name="Exe_actXServerName" Type="Str">TestReadTemperature</Property>
				<Property Name="Exe_actXServerNameGUID" Type="Str"></Property>
				<Property Name="Source[0].itemID" Type="Str">{5704CF59-65F4-4938-8321-C94F2C2286EC}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/test read temperature.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
			</Item>
		</Item>
	</Item>
</Project>
