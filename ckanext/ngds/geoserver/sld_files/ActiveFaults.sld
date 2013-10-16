<?xml version="1.0" encoding="ISO-8859-1"?>
<sld:StyledLayerDescriptor xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
	<sld:NamedLayer>
		<sld:Name><![CDATA[ActiveFault]]></sld:Name>
		<sld:UserStyle>
		<sld:Title>Quaternary (Active) Faults</sld:Title>
		<sld:Abstract>Quaternary active faults styled layer descriptor for providing ngds services using defined layer symbolization schemes.</sld:Abstract>
			<sld:FeatureTypeStyle>
				<sld:Rule>
					<sld:Name><![CDATA[Historic (<150 yrs)]]></sld:Name>
					<sld:Title><![CDATA[Historic (<150 yrs)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.1]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#ff0000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >1</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Holocene (<10 ka)]]></sld:Name>
					<sld:Title><![CDATA[Holocene (<10 ka)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.2]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#ffaa00</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.5</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Late Quaternary (750 ka)]]></sld:Name>
					<sld:Title><![CDATA[Late Quaternary (750 ka)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.3]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#55ff00</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.5</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Late Pleistocene (<1.6 ma)]]></sld:Name>
					<sld:Title><![CDATA[Late Pleistocene (<1.6 ma)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.3a]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#0070ff</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.666666666666667</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Early Pleistocene (<2.8 ma)]]></sld:Name>
					<sld:Title><![CDATA[Early Pleistocene (<2.8 ma)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.3b]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#b2b2b2</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >1</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Quaternary (Undifferentiated)]]></sld:Name>
					<sld:Title><![CDATA[Quaternary (Undifferentiated)]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[2.13.4]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#aa87eb</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >2</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >0.75</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[Fault]]></sld:Name>
					<sld:Title><![CDATA[Fault]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>Symbol</ogc:PropertyName>
							<ogc:Literal><![CDATA[Class B]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<sld:LineSymbolizer>
						<sld:Stroke>
							<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
							<sld:CssParameter name="stroke-width" >1</sld:CssParameter>
							<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
						</sld:Stroke>
					</sld:LineSymbolizer>
				</sld:Rule>
			</sld:FeatureTypeStyle>
		</sld:UserStyle>
	</sld:NamedLayer>
</sld:StyledLayerDescriptor>
