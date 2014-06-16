/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
describe("L.LatLngUtil", function () {
	it("cloneLatLngs", function () {
		var latLngs = [{ lat: 0, lng: 0 }],
			clone = L.LatLngUtil.cloneLatLngs(latLngs);

		expect(clone[0].lat).to.eql(latLngs[0].lat);

		clone[0].lat = 10;
		expect(latLngs[0].lat).to.eql(0);
	});
});
