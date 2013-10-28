<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
	<sld:NamedLayer>
		<sld:Name>Hypocenter</sld:Name>
		<UserStyle xmlns="http://www.opengis.net/sld">
		<FeatureTypeStyle>
			<Rule>
				<Name><![CDATA[0 - 1 Magnitude]]></Name>
				<Title><![CDATA[0 - 1 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>0.9</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>1</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
				<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude01.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[1 - 2 Magnitude]]></Name>
				<Title><![CDATA[1 - 2 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>1</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>2</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude12.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[2 - 3 Magnitude]]></Name>
				<Title><![CDATA[2 - 3 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>2</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>3</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude23.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[3 - 4 Magnitude]]></Name>
				<Title><![CDATA[3 - 4 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>3</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>4</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude34.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[4 - 5 Magnitude]]></Name>
				<Title><![CDATA[4 - 5 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>4</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>5</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude45.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[5 - 6 Magnitude]]></Name>
				<Title><![CDATA[5 - 6 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>5</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>6</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude56.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[6 - 7 Magnitude]]></Name>
				<Title><![CDATA[6 - 7 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>6</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>7</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude67.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[7 - 8 Magnitude]]></Name>
				<Title><![CDATA[7 - 8 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>7</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>8</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude78.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			<Rule>
				<Name><![CDATA[8 - 9 Magnitude]]></Name>
				<Title><![CDATA[8 - 9 Magnitude]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsBetween>
							<ogc:PropertyName>Magnitude</ogc:PropertyName>
							<ogc:LowerBoundary>
								<ogc:Literal>8</ogc:Literal>
							</ogc:LowerBoundary>
							<ogc:UpperBoundary>
								<ogc:Literal>9</ogc:Literal>
							</ogc:UpperBoundary>	
						</ogc:PropertyIsBetween>
					</ogc:Filter>
			<PointSymbolizer>
				<Graphic>
					<ExternalGraphic>
						<OnlineResource
								xmlns:xlink="http://www.w3.org/1999/xlink"
								xlink:type="simple"
								xlink:href="http://schemas.usgin.org/schemas/slds/ngds_symbols/Magnitude89.png"/>
							<Format>image/png</Format>
						</ExternalGraphic>
						<Size>4</Size>
					</Graphic>
				</PointSymbolizer>
			</Rule>
			</FeatureTypeStyle>
		</UserStyle>
	</sld:NamedLayer>
</sld:StyledLayerDescriptor>