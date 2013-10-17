<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
	<sld:NamedLayer>
		<sld:Name><![CDATA[GeothermalArea]]></sld:Name>
		<sld:UserStyle>
			<sld:FeatureTypeStyle>
				<sld:Rule>
					<sld:Name><![CDATA[High temperature]]></sld:Name>
					<sld:Title><![CDATA[High temperature]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>GeothermTempCharacterization</ogc:PropertyName>
							<ogc:Literal><![CDATA[High temperature]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:PolygonSymbolizer>
						<sld:Fill>
							<sld:CssParameter name="fill" >#ffbebe</sld:CssParameter>
							<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
						</sld:Fill>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#ff0000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.4</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:PolygonSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Low temperature]]></sld:Name>
					<sld:Title><![CDATA[Low temperature]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>GeothermTempCharacterization</ogc:PropertyName>
							<ogc:Literal><![CDATA[Low temperature]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:PolygonSymbolizer>
						<sld:Fill>
							<sld:CssParameter name="fill" >#ffebaf</sld:CssParameter>
							<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
						</sld:Fill>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#ffaa00</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.4</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:PolygonSymbolizer>
				</sld:Rule>
			</sld:FeatureTypeStyle>
		</sld:UserStyle>
	</sld:NamedLayer>
</sld:StyledLayerDescriptor>
