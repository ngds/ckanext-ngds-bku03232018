<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor xmlns:xlink='http://www.w3.org/1999/xlink' xmlns:gml='http://www.opengis.net/gml' xmlns:ogc='http://www.opengis.net/ogc' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' version='1.0.0' xsi:schemaLocation='http://www.opengis.net/sld StyledLayerDescriptor.xsd' xmlns='http://www.opengis.net/sld' xmlns:gsmlp='http://xmlns.geosciml.org/geosciml-portrayal/2.0'  >
	<NamedLayer>
		<Name><![CDATA[gsmlp:ContactView]]></Name>
		<Title>Symbology for OneGeology GeoSciML-Portrayal Contact View Layer</Title>
		<Description>Styled for use in the OneGeology GeoSciML-Portrayal Contact View layer, this assumes that the data adhears to FGDC (Federal Geographic Data Committee) codes which defines spatial standards for the United States in its Content Standard for Digital Geospatial Metadata (www.fgdc.gov_). This symbology describes accurately and approximately located as well as concealed contacts.</Description>
		<UserStyle>
			<FeatureTypeStyle>
				<Rule>
					<Name><![CDATA[contact, accurately located]]></Name>
					<Title><![CDATA[contact, accurately located]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbology</ogc:PropertyName>
							<ogc:Literal><![CDATA[1.1.1]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >1</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
							<CssParameter name="stroke-linejoin" >mitre</CssParameter>
							<CssParameter name="stroke-linecap" >butt</CssParameter>
						</Stroke>
					</LineSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[contact, approximately located]]></Name>
					<Title><![CDATA[contact, approximately located]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbology</ogc:PropertyName>
							<ogc:Literal><![CDATA[1.1.3]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >1</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
							<CssParameter name="stroke-linejoin" >mitre</CssParameter>
							<CssParameter name="stroke-linecap" >butt</CssParameter>
							<CssParameter name="stroke-dasharray" >9 3</CssParameter>
							<CssParameter name="stroke-dashoffset" >0</CssParameter>
						</Stroke>
					</LineSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[contact, concealed]]></Name>
					<Title><![CDATA[contact, concealed]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbology</ogc:PropertyName>
							<ogc:Literal><![CDATA[1.1.7]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >1</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
							<CssParameter name="stroke-linejoin" >mitre</CssParameter>
							<CssParameter name="stroke-linecap" >butt</CssParameter>
							<CssParameter name="stroke-dasharray" >3 3</CssParameter>
							<CssParameter name="stroke-dashoffset" >0</CssParameter>
						</Stroke>
					</LineSymbolizer>
				</Rule>
			</FeatureTypeStyle>
		</UserStyle>
	</NamedLayer>
</StyledLayerDescriptor>
