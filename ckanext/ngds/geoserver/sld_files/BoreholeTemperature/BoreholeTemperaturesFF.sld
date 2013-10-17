<?xml version="1.0" encoding="ISO-8859-1"?>
<sld:StyledLayerDescriptor xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
	<sld:NamedLayer>
		<sld:Name><![CDATA[BoreholeTemperature]]></sld:Name>
		<sld:UserStyle>
			<sld:FeatureTypeStyle>
				<sld:Rule>
					<sld:Name><![CDATA[< 95 F]]></sld:Name>
					<sld:Title><![CDATA[< 95 F]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>MeasuredTemperature</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>21.7</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>95</ogc:Literal>
							</ogc:UpperBoundary>
						</ogc:PropertyIsBetween>
					</ogc:Filter>
					<sld:PointSymbolizer>
						<sld:Graphic>
							<sld:Mark>
								<sld:WellKnownName>circle</sld:WellKnownName>
								<sld:Fill>
									<sld:CssParameter name="fill" >#38a800</sld:CssParameter>
									<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
								</sld:Fill>
								<sld:Stroke>
									<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
									<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
								</sld:Stroke>
							</sld:Mark>
								<sld:Size>4</sld:Size>
						</sld:Graphic>
					</sld:PointSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[95 - 113]]></sld:Name>
					<sld:Title><![CDATA[95 - 113]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>MeasuredTemperature</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>95</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>113</ogc:Literal>
							</ogc:UpperBoundary>
						</ogc:PropertyIsBetween>
					</ogc:Filter>
					<sld:PointSymbolizer>
						<sld:Graphic>
							<sld:Mark>
								<sld:WellKnownName>circle</sld:WellKnownName>
								<sld:Fill>
									<sld:CssParameter name="fill" >#8bd100</sld:CssParameter>
									<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
								</sld:Fill>
								<sld:Stroke>
									<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
									<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
								</sld:Stroke>
							</sld:Mark>
							<sld:Size>4</sld:Size>
						</sld:Graphic>
					</sld:PointSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[113 - 140 ]]></sld:Name>
					<sld:Title><![CDATA[113 - 140 ]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>MeasuredTemperature</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>113</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>140</ogc:Literal>
							</ogc:UpperBoundary>
						</ogc:PropertyIsBetween>
					</ogc:Filter>
					<sld:PointSymbolizer>
						<sld:Graphic>
							<sld:Mark>
								<sld:WellKnownName>circle</sld:WellKnownName>
								<sld:Fill>
									<sld:CssParameter name="fill" >#ffff00</sld:CssParameter>
									<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
								</sld:Fill>
								<sld:Stroke>
									<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
									<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
								</sld:Stroke>
							</sld:Mark>
							<sld:Size>4</sld:Size>
						</sld:Graphic>
					</sld:PointSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[140 - 212]]></sld:Name>
					<sld:Title><![CDATA[140 - 212]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>MeasuredTemperature</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>140</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>212</ogc:Literal>
							</ogc:UpperBoundary>
						</ogc:PropertyIsBetween>
					</ogc:Filter>
					<sld:PointSymbolizer>
						<sld:Graphic>
							<sld:Mark>
								<sld:WellKnownName>circle</sld:WellKnownName>
								<sld:Fill>
									<sld:CssParameter name="fill" >#ff8000</sld:CssParameter>
									<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
								</sld:Fill>
								<sld:Stroke>
									<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
									<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
								</sld:Stroke>
							</sld:Mark>
							<sld:Size>4</sld:Size>
						</sld:Graphic>
					</sld:PointSymbolizer>
				</sld:Rule>
				<sld:Rule>
					<sld:Name><![CDATA[=> 212]]></sld:Name>
					<sld:Title><![CDATA[=> 212]]></sld:Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>MeasuredTemperature</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>212</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>1000</ogc:Literal>
							</ogc:UpperBoundary>
						</ogc:PropertyIsBetween>
					</ogc:Filter>
					<sld:PointSymbolizer>
						<sld:Graphic>
							<sld:Mark>
								<sld:WellKnownName>circle</sld:WellKnownName>
								<sld:Fill>
									<sld:CssParameter name="fill" >#ff0000</sld:CssParameter>
									<sld:CssParameter name="fill-opacity" >1</sld:CssParameter>
								</sld:Fill>
								<sld:Stroke>
									<sld:CssParameter name="stroke" >#000000</sld:CssParameter>
									<sld:CssParameter name="stroke-opacity" >1</sld:CssParameter>
								</sld:Stroke>
							</sld:Mark>
							<sld:Size>4</sld:Size>
						</sld:Graphic>
					</sld:PointSymbolizer>
				</sld:Rule>
			</sld:FeatureTypeStyle>
		</sld:UserStyle>
	</sld:NamedLayer>
</sld:StyledLayerDescriptor>
