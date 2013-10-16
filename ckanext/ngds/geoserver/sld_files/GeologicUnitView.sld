<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor xmlns:xlink='http://www.w3.org/1999/xlink' xmlns:gml='http://www.opengis.net/gml' xmlns:ogc='http://www.opengis.net/ogc' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' version='1.0.0' xsi:schemaLocation='http://www.opengis.net/sld StyledLayerDescriptor.xsd' xmlns='http://www.opengis.net/sld' xmlns:gsmlp='http://xmlns.geosciml.org/geosciml-portrayal/2.0' >
	<NamedLayer>
		<Name><![CDATA[gsmlp:GeologicUnitView]]></Name>
		<Title>Symbology for OneGeology GeoSciML-Portrayal Geologic Unit View Layer</Title>
		<Description>Styled for use in the OneGeology GeoSciML-Portrayal Geologic Unit View layer, this assumes that the data implements the GeologicUnitType201202  URIs in the representativeAge_uri field. URIs are outlined in the content model available at http://schemas.usgin.org/files/geologic-units/2.0/GeoSciML.xlsx. This symbology describes geologic ages with specific RGB color values according to the 2013 ICS (International Commission on Stratigraphy) time scale (http://www.stratigraphy.org/index.php/ics-chart-timescale).</Description>
		<UserStyle>
			<FeatureTypeStyle>
				<Rule>
					<Name><![CDATA[Phanerozoic]]></Name>
					<Title><![CDATA[Phanerozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Phanerozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#9ad9dd</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cenozoic]]></Name>
					<Title><![CDATA[Cenozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cenozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f2f91d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Quaternary]]></Name>
					<Title><![CDATA[Quaternary]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Quaternary]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f9f97f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Holocene]]></Name>
					<Title><![CDATA[Holocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Holocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fef2e0</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pleistocene]]></Name>
					<Title><![CDATA[Pleistocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pleistocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fff2ae</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Pleistocene]]></Name>
					<Title><![CDATA[Upper Pleistocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperPleistocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fff2d3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Pleistocene]]></Name>
					<Title><![CDATA[Middle Pleistocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ionian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fff2c7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Calabrian]]></Name>
					<Title><![CDATA[Calabrian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Calabrian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fff2ba</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Gelasian]]></Name>
					<Title><![CDATA[Gelasian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Gelasian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffedb3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Neogene]]></Name>
					<Title><![CDATA[Neogene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Neogene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffe619</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pliocene]]></Name>
					<Title><![CDATA[Pliocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pliocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff99</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Piacenzian]]></Name>
					<Title><![CDATA[Piacenzian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Piacenzian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffffbf</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Zanclean]]></Name>
					<Title><![CDATA[Zanclean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Zanclean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffffb3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Miocene]]></Name>
					<Title><![CDATA[Miocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Miocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff00</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Messinian]]></Name>
					<Title><![CDATA[Messinian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Messinian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff73</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Tortonian]]></Name>
					<Title><![CDATA[Tortonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Tortonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff66</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Serravallian]]></Name>
					<Title><![CDATA[Serravallian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Serravallian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff59</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Langhian]]></Name>
					<Title><![CDATA[Langhian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Langhian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff4d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Burdigalian]]></Name>
					<Title><![CDATA[Burdigalian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Burdigalian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff41</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Aquitanian]]></Name>
					<Title><![CDATA[Aquitanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Aquitanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ffff33</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paleogene]]></Name>
					<Title><![CDATA[Paleogene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paleogene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fd9a52</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Oligocene]]></Name>
					<Title><![CDATA[Oligocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Oligocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdc07a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Chattian]]></Name>
					<Title><![CDATA[Chattian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Chattian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fee6aa</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Rupelian]]></Name>
					<Title><![CDATA[Rupelian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Rupelian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fed99a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Eocene]]></Name>
					<Title><![CDATA[Eocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Eocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdb46c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Priabonian]]></Name>
					<Title><![CDATA[Priabonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Priabonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdcda1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Bartonian]]></Name>
					<Title><![CDATA[Bartonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Bartonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdc091</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lutetian]]></Name>
					<Title><![CDATA[Lutetian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Lutetian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fcb482</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ypresian]]></Name>
					<Title><![CDATA[Ypresian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ypresian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fca773</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paleocene]]></Name>
					<Title><![CDATA[Paleocene]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paleocene]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fda75f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Thanetian]]></Name>
					<Title><![CDATA[Thanetian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Thanetian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdbf6f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Selandian]]></Name>
					<Title><![CDATA[Selandian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Selandian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#febf65</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Danian]]></Name>
					<Title><![CDATA[Danian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Danian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdb462</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Mesozoic]]></Name>
					<Title><![CDATA[Mesozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Mesozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#67c5ca</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cretaceous]]></Name>
					<Title><![CDATA[Cretaceous]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cretaceous]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#7fc64e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Cretaceous]]></Name>
					<Title><![CDATA[Upper Cretaceous]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperCretaceous]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6d84a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Maastrichtian]]></Name>
					<Title><![CDATA[Maastrichtian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Maastrichtian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f2fa8c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Campanian]]></Name>
					<Title><![CDATA[Campanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Campanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e6f47f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Santonian]]></Name>
					<Title><![CDATA[Santonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Santonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#d9ef74</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Coniacian]]></Name>
					<Title><![CDATA[Coniacian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Coniacian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#cce968</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Turonian]]></Name>
					<Title><![CDATA[Turonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Turonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe35d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cenomanian]]></Name>
					<Title><![CDATA[Cenomanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cenomanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3de53</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Cretaceous]]></Name>
					<Title><![CDATA[Lower Cretaceous]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerCretaceous]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8ccd57</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Albian]]></Name>
					<Title><![CDATA[Albian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Albian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccea97</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Aptian]]></Name>
					<Title><![CDATA[Aptian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Aptian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe48a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Barremian]]></Name>
					<Title><![CDATA[Barremian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Barremian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3df7f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Hauterivian]]></Name>
					<Title><![CDATA[Hauterivian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Hauterivian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6d975</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Valanginian]]></Name>
					<Title><![CDATA[Valanginian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Valanginian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99d36a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Berriasian]]></Name>
					<Title><![CDATA[Berriasian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Berriasian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8ccd60</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Jurassic]]></Name>
					<Title><![CDATA[Jurassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Jurassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#34b2c9</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Jurassic]]></Name>
					<Title><![CDATA[Upper Jurassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperJurassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e3ee</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Tithonian]]></Name>
					<Title><![CDATA[Tithonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Tithonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#d9f1f7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Kimmeridgian]]></Name>
					<Title><![CDATA[Kimmeridgian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Kimmeridgian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccecf4</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Oxfordian]]></Name>
					<Title><![CDATA[Oxfordian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Oxfordian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe7f1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Jurassic]]></Name>
					<Title><![CDATA[Middle Jurassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddleJurassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#80cfd8</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Callovian]]></Name>
					<Title><![CDATA[Callovian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Callovian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe7e5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Bathonian]]></Name>
					<Title><![CDATA[Bathonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Bathonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e2e3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Bajocian]]></Name>
					<Title><![CDATA[Bajocian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Bajocian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6dde0</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Aalenian]]></Name>
					<Title><![CDATA[Aalenian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Aalenian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#9ad9dd</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Jurassic]]></Name>
					<Title><![CDATA[Lower Jurassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerJurassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#42aed0</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Toarcian]]></Name>
					<Title><![CDATA[Toarcian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Toarcian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99cee3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pliensbachian]]></Name>
					<Title><![CDATA[Pliensbachian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pliensbachian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#80c5dd</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Sinemurian]]></Name>
					<Title><![CDATA[Sinemurian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Sinemurian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#67bcd8</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Hettangian]]></Name>
					<Title><![CDATA[Hettangian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Hettangian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#4eb3d3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Triassic]]></Name>
					<Title><![CDATA[Triassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Triassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#812b92</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Triassic]]></Name>
					<Title><![CDATA[Upper Triassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperTriassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bd8cc3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Rhaetian]]></Name>
					<Title><![CDATA[Rhaetian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Rhaetian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e3b9db</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Norian]]></Name>
					<Title><![CDATA[Norian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Norian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#d6aad3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Carnian]]></Name>
					<Title><![CDATA[Carnian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Carnian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#c99bcb</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Triassic]]></Name>
					<Title><![CDATA[Middle Triassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddleTriassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b168b1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ladinian]]></Name>
					<Title><![CDATA[Ladinian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ladinian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#c983bf</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Anisian]]></Name>
					<Title><![CDATA[Anisian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Anisian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bc75b7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Triassic]]></Name>
					<Title><![CDATA[Lower Triassic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerTriassic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#983999</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Olenekian]]></Name>
					<Title><![CDATA[Olenekian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Olenekian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b051a5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Induan]]></Name>
					<Title><![CDATA[Induan]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Induan]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a4469f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paleozoic]]></Name>
					<Title><![CDATA[Paleozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paleozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99c08d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Permian]]></Name>
					<Title><![CDATA[Permian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Permian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f04028</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lopingian]]></Name>
					<Title><![CDATA[Lopingian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Lopingian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fba794</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Changhsingian]]></Name>
					<Title><![CDATA[Changhsingian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Changhsingian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fcc0b2</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Wuchiapingian]]></Name>
					<Title><![CDATA[Wuchiapingian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Wuchiapingian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fcb4a2</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Guadalupian]]></Name>
					<Title><![CDATA[Guadalupian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Guadalupian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fb745c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Capitanian]]></Name>
					<Title><![CDATA[Capitanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Capitanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fb9a85</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Wordian]]></Name>
					<Title><![CDATA[Wordian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Wordian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fb8d76</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Roadian]]></Name>
					<Title><![CDATA[Roadian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Roadian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fb8069</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cisuralian]]></Name>
					<Title><![CDATA[Cisuralian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cisuralian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ef5845</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Kungurian]]></Name>
					<Title><![CDATA[Kungurian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Kungurian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e38776</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Artinskian]]></Name>
					<Title><![CDATA[Artinskian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Artinskian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e37b68</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Sakmarian]]></Name>
					<Title><![CDATA[Sakmarian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Sakmarian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e36f5c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Asselian]]></Name>
					<Title><![CDATA[Asselian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Asselian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e36350</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Carboniferous]]></Name>
					<Title><![CDATA[Carboniferous]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Carboniferous]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#67a599</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pennsylvanian]]></Name>
					<Title><![CDATA[Pennsylvanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pennsylvanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99c2b5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Pennsylvanian]]></Name>
					<Title><![CDATA[Upper Pennsylvanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperPennsylvanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfd0ba</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Gzhelian]]></Name>
					<Title><![CDATA[Gzhelian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Gzhelian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccd4c7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Kasimovian]]></Name>
					<Title><![CDATA[Kasimovian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Kasimovian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfd0c5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Pennsylvanian]]></Name>
					<Title><![CDATA[Middle Pennsylvanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddlePennsylvanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6c7b7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Moscovian]]></Name>
					<Title><![CDATA[Moscovian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Moscovian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3cbb9</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Pennsylvanian]]></Name>
					<Title><![CDATA[Lower Pennsylvanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerPennsylvanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8cbeb4</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Bashkirian]]></Name>
					<Title><![CDATA[Bashkirian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Bashkirian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99c2b5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Mississippian]]></Name>
					<Title><![CDATA[Mississippian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Mississippian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#678f66</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Mississippian]]></Name>
					<Title><![CDATA[Upper Mississippian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperMississippian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3be6c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Serpukhovian]]></Name>
					<Title><![CDATA[Serpukhovian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Serpukhovian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfc26b</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Mississippian]]></Name>
					<Title><![CDATA[Middle Mississippian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddleMississippian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99b46c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Visean]]></Name>
					<Title><![CDATA[Visean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Visean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6b96c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Mississippian]]></Name>
					<Title><![CDATA[Lower Mississippian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerMississippian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#80ab6c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Tournaisian]]></Name>
					<Title><![CDATA[Tournaisian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Tournaisian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8cb06c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Devonian]]></Name>
					<Title><![CDATA[Devonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Devonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#cb8c37</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Devonian]]></Name>
					<Title><![CDATA[Upper Devonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperDevonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f1e19d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Famennian]]></Name>
					<Title><![CDATA[Famennian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Famennian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f2edc5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Frasnian]]></Name>
					<Title><![CDATA[Frasnian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Frasnian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f2edad</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Devonian]]></Name>
					<Title><![CDATA[Middle Devonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddleDevonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f1c868</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Givetian]]></Name>
					<Title><![CDATA[Givetian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Givetian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f1e185</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Eifelian]]></Name>
					<Title><![CDATA[Eifelian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Eifelian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f1d576</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Devonian]]></Name>
					<Title><![CDATA[Lower Devonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerDevonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e5ac4d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Emsian]]></Name>
					<Title><![CDATA[Emsian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Emsian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e5d075</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pragian]]></Name>
					<Title><![CDATA[Pragian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pragian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e5c468</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lochkovian]]></Name>
					<Title><![CDATA[Lochkovian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Lochkovian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e5b75a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Silurian]]></Name>
					<Title><![CDATA[Silurian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Silurian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e1b6</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Pridoli]]></Name>
					<Title><![CDATA[Pridoli]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Pridoli]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e6f5e1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ludlow]]></Name>
					<Title><![CDATA[Ludlow]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ludlow]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe6cf</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ludfordian]]></Name>
					<Title><![CDATA[Ludfordian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ludfordian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#d9f0df</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Gorstian]]></Name>
					<Title><![CDATA[Gorstian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Gorstian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccecdd</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Wenlock]]></Name>
					<Title><![CDATA[Wenlock]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Wenlock]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e1c2</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Homerian]]></Name>
					<Title><![CDATA[Homerian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Homerian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccebd1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Sheinwoodian]]></Name>
					<Title><![CDATA[Sheinwoodian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Sheinwoodian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe6c3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Llandovery]]></Name>
					<Title><![CDATA[Llandovery]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Llandovery]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99d7b3</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Telychian]]></Name>
					<Title><![CDATA[Telychian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Telychian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfe6cf</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Aeronian]]></Name>
					<Title><![CDATA[Aeronian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Aeronian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e1c2</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Rhuddanian]]></Name>
					<Title><![CDATA[Rhuddanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Rhuddanian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6dcb5</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ordovician]]></Name>
					<Title><![CDATA[Ordovician]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ordovician]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#009270</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Upper Ordovician]]></Name>
					<Title><![CDATA[Upper Ordovician]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/UpperOrdovician]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#7fca93</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Hirnantian]]></Name>
					<Title><![CDATA[Hirnantian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Hirnantian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6dbab</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Katian]]></Name>
					<Title><![CDATA[Katian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Katian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99d69f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Sandbian]]></Name>
					<Title><![CDATA[Sandbian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Sandbian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8cd094</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Middle Ordovician]]></Name>
					<Title><![CDATA[Middle Ordovician]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/MiddleOrdovician]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#4db47e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Darriwilian]]></Name>
					<Title><![CDATA[Darriwilian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Darriwilian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#74c69c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Dapingian]]></Name>
					<Title><![CDATA[Dapingian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Dapingian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#66c092</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Lower Ordovician]]></Name>
					<Title><![CDATA[Lower Ordovician]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/LowerOrdovician]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#1a9d6f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Floian]]></Name>
					<Title><![CDATA[Floian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Floian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#41b087</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Tremadocian]]></Name>
					<Title><![CDATA[Tremadocian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Tremadocian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#33a97e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian]]></Name>
					<Title><![CDATA[Cambrian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cambrian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#7fa056</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Furongian]]></Name>
					<Title><![CDATA[Furongian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Furongian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3e095</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Stage 10]]></Name>
					<Title><![CDATA[Cambrian Stage 10]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage10]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#e6f5c9</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Jiangshanian]]></Name>
					<Title><![CDATA[Jiangshanian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage9]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#d9f0bb</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paibian]]></Name>
					<Title><![CDATA[Paibian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paibian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccebae</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Series 3]]></Name>
					<Title><![CDATA[Cambrian Series 3]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianSeries3]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6cf86</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Guzhangian]]></Name>
					<Title><![CDATA[Guzhangian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Guzhangian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ccdfaa</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Drumian]]></Name>
					<Title><![CDATA[Drumian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Drumian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#bfd99d</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Stage 5]]></Name>
					<Title><![CDATA[Cambrian Stage 5]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage5]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3d492</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Series 2]]></Name>
					<Title><![CDATA[Cambrian Series 2]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianSeries2]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99c078</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Stage 4]]></Name>
					<Title><![CDATA[Cambrian Stage 4]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage4]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#b3ca8e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Stage 3]]></Name>
					<Title><![CDATA[Cambrian Stage 3]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage3]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6c583</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Terreneuvian]]></Name>
					<Title><![CDATA[Terreneuvian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Terreneuvian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#8cb06c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cambrian Stage 2]]></Name>
					<Title><![CDATA[Cambrian Stage 2]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/CambrianStage2]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#a6ba80</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Fortunian]]></Name>
					<Title><![CDATA[Fortunian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Fortunian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#99b575</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Precambrian]]></Name>
					<Title><![CDATA[Precambrian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Precambrian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f74370</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Proterozoic]]></Name>
					<Title><![CDATA[Proterozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Proterozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f73563</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Neoproterozoic]]></Name>
					<Title><![CDATA[Neoproterozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Neoproterozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#feb342</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ediacaran]]></Name>
					<Title><![CDATA[Ediacaran]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ediacaran]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fed96a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Cryogenian]]></Name>
					<Title><![CDATA[Cryogenian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Cryogenian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fecc5c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Tonian]]></Name>
					<Title><![CDATA[Tonian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Tonian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#febf4e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Mesoproterozoic]]></Name>
					<Title><![CDATA[Mesoproterozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Mesoproterozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdb462</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Stenian]]></Name>
					<Title><![CDATA[Stenian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Stenian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fed99a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Ectasian]]></Name>
					<Title><![CDATA[Ectasian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Ectasian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdcc8a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Calymmian]]></Name>
					<Title><![CDATA[Calymmian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Calymmian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#fdc07a</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paleoproterozoic]]></Name>
					<Title><![CDATA[Paleoproterozoic]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paleoproterozoic]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f74370</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Statherian]]></Name>
					<Title><![CDATA[Statherian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Statherian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f875a7</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Orosirian]]></Name>
					<Title><![CDATA[Orosirian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Orosirian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f76898</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Rhyacian]]></Name>
					<Title><![CDATA[Rhyacian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Rhyacian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f75b89</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Siderian]]></Name>
					<Title><![CDATA[Siderian]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Siderian]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f74f7c</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Archaean]]></Name>
					<Title><![CDATA[Archaean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Archean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f0047f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Neoarchean]]></Name>
					<Title><![CDATA[Neoarchean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Neoarchean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f99bc1</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Mesoarchean]]></Name>
					<Title><![CDATA[Mesoarchean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Mesoarchean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f768a9</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Paleoarchean]]></Name>
					<Title><![CDATA[Paleoarchean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Paleoarchean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#f4449f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Eoarchean]]></Name>
					<Title><![CDATA[Eoarchean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Eoarchean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#da037f</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
				<Rule>
					<Name><![CDATA[Hadean]]></Name>
					<Title><![CDATA[Hadean]]></Title>
					<ogc:Filter>
						<ogc:PropertyIsEqualTo>
							<ogc:PropertyName>gsmlp:representativeAge_uri</ogc:PropertyName>
							<ogc:Literal><![CDATA[http://resource.geosciml.org/classifier/ics/ischart/Hadean]]></ogc:Literal>
						</ogc:PropertyIsEqualTo>
					</ogc:Filter>
					<PolygonSymbolizer>
						<Fill>
							<CssParameter name="fill" >#ae027e</CssParameter>
							<CssParameter name="fill-opacity" >1</CssParameter>
						</Fill>
						<Stroke>
							<CssParameter name="stroke" >#000000</CssParameter>
							<CssParameter name="stroke-width" >0.4</CssParameter>
							<CssParameter name="stroke-opacity" >1</CssParameter>
						</Stroke>
					</PolygonSymbolizer>
				</Rule>
			</FeatureTypeStyle>
		</UserStyle>
	</NamedLayer>
</StyledLayerDescriptor>
