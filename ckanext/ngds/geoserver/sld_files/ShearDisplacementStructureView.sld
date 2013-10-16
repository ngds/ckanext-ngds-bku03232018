<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor xmlns:xlink='http://www.w3.org/1999/xlink' xmlns:gml='http://www.opengis.net/gml' xmlns:ogc='http://www.opengis.net/ogc' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' version='1.0.0' xsi:schemaLocation='http://www.opengis.net/sld StyledLayerDescriptor.xsd' xmlns='http://www.opengis.net/sld' xmlns:gsmlp='http://xmlns.geosciml.org/geosciml-portrayal/2.0' >
	<NamedLayer>
		<Name><![CDATA[gsmlp:ShearDisplacementStructureView]]></Name>
		<Title>Symbology for OneGeology GeoSciML-Portrayal Shear Displacement Structure View Layer</Title>
		<Description>Styled for use in the OneGeology GeoSciML-Portrayal Shear Displacement Structure View layer, this assumes that the data adhears to FGDC (Federal Geographic Data Committee) codes which defines spatial standards for the United States in its Content Standard for Digital Geospatial Metadata (www.fgdc.gov/). This symbology describes accurately and approximately located as well as concealed faults.</Description>
		<UserStyle>
			<FeatureTypeStyle>
			<Rule>
					<Name><![CDATA[fault, accurately located]]></Name>
					<Title><![CDATA[fault, accurately located]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbolizer</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.1.1]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >2</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
							<CssParameter name="stroke-linejoin" >mitre</CssParameter>
							<CssParameter name="stroke-linecap" >butt</CssParameter>
						</Stroke>
					</LineSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[fault, approximately located]]></Name>
					<Title><![CDATA[fault, approximately located]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbolizer</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.1.3]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >2</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
							<CssParameter name="stroke-linejoin" >mitre</CssParameter>
							<CssParameter name="stroke-linecap" >butt</CssParameter>
							<CssParameter name="stroke-dasharray" >9 3</CssParameter>
							<CssParameter name="stroke-dashoffset" >0</CssParameter>
						</Stroke>
					</LineSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[fault, concealed]]></Name>
					<Title><![CDATA[fault, concealed]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>genericSymbolizer</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.1.7]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<LineSymbolizer>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >2</CssParameter>
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
