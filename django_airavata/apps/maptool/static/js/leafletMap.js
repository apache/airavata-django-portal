L.CursorHandler = L.Handler.extend({

    addHooks: function () {
        this._popup = new L.Popup();
        this._map.on('mouseover', this._open, this);
        this._map.on('mousemove', this._update, this);
        this._map.on('mouseout', this._close, this);
    },

    removeHooks: function () {
        this._map.off('mouseover', this._open, this);
        this._map.off('mousemove', this._update, this);
        this._map.off('mouseout', this._close, this);
    },

    _open: function (e) {
        this._update(e);
        this._popup.openOn(this._map);
    },

    _close: function () {
        this._map.closePopup(this._popup);
    },

    _update: function (e) {
        this._popup.setLatLng(e.latlng)
            .setContent(e.latlng.toString());
    }


});
L.Map.addInitHook('addHandler', 'cursor', L.CursorHandler);
map = L.map('map',{cursor:true}).setView([38.420836729,-87.762496593], 8);
// map=L.map('leaflet',{
//     center:[38.420836729,-87.762496593],
//     zoom:7,
//     cursor:true
// });

    osmUrl='//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    osm = new L.TileLayer(osmUrl, {minZoom: 1, maxZoom: 15, attribution: osmAttrib});
    map.addLayer(osm);
    //Draw the cost area of 80km
    var boundry_circle_options={

        fillColor:"#229954",
        fillOpacity:0.6,
        color:"#229954"
    };
    // L.circle([ 38.3689,-87.7659 ],80000,boundry_circle_options).addTo(map)
    bound_layer=L.circle([ 38.3689,-87.7659 ],80000,boundry_circle_options);


    // L.geoJson(path).addTo(map);

    // console.log(source_sink.length);
    // L.geoJson(source_sink).addTo(map);
    // source_sink_layer=L.geoJson(source_sonk,{
    //     pointToLayer:function(feature,latlng){
    //         return L.circleMarker(latlng,geojsonMarkerOptions).bindPopup('Source Sink');;
    //     }
    // });







    var chemicalClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Chemicals.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            chemicalClusters.addLayer(m);

        }

    });

    var coalClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Coal-based_Liquid_Fuel_Supply.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            coalClusters.addLayer(m);

        }

    });

    var flourinatedClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Import_and_Export_of_Equipment_Containing_Fluorintaed_GHGs.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            flourinatedClusters.addLayer(m);

        }

    });

    var industrialGasClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Industrial_Gas_Suppliers.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            industrialGasClusters.addLayer(m);

        }

    });

    var co2InjectionClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Injection_of_CO2.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            co2InjectionClusters.addLayer(m);

        }

    });

    var metalClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Metals.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            metalClusters.addLayer(m);

        }

    });

    var mineralClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Minerals.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            mineralClusters.addLayer(m);

        }

    });

    var naturalGasClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Natural_Gas_and_Natural_Gas_Liquids_Suppliers.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            naturalGasClusters.addLayer(m);

        }

    });

    var otherClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Other.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            otherClusters.addLayer(m);

        }

    });

    var petroleumClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Petroleum_Product_Suppliers.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            petroleumClusters.addLayer(m);

        }

    });

    var petroleumNaturalGasClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Petroleum_and_Natural_Gas_Systems.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            petroleumNaturalGasClusters.addLayer(m);

        }

    });

    var powerPlantClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Power_Plants.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            powerPlantClusters.addLayer(m);

        }

    });
    var pulpClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Pulp_and_Paper.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            pulpClusters.addLayer(m);

        }

    });

    var refineriesClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Refineries.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            refineriesClusters.addLayer(m);

        }

    });

    var co2SupplyClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Pulp_and_Paper.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            co2SupplyClusters.addLayer(m);

        }

    });

    var wasteClusters=L.markerClusterGroup();
    $.getJSON('/static/Data/Source_Refineries.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='<br><b>Facility</b>:'+data[i].properties.Facility_N+
                '<br/><b>Place</b>:'+data[i].properties.City+
                '<br/><b>IndustryType</b> :' + data[i].properties.Industry_T +
              '<br/><b>Co2 Emission</b> :' + data[i].properties.CO2_Emissi;



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            wasteClusters.addLayer(m);

        }

    });

    var ordos_source_cluster=L.markerClusterGroup();
    $.getJSON('/static/Data/Ordos_Basin_Source.json',function (data) {


        for(var i=0;i<data.length;i++){
            var popup='Sink Nos# '+(i+1);



            var m=L.marker([data[i].geometry.coordinates[1],data[i].geometry.coordinates[0]]).bindPopup(popup);
            ordos_source_cluster.addLayer(m);

        }

    });
    // map.addLayer(ordos_source_cluster);


    // map.addLayer(france_source_cluster);







//     var sink_saline_polygon;
//     $.getJSON('/static/Data/Sinks_NATCARB_SALINE_For_Gateway.json',function (data) {
//
//         var geojsonMarkerOptions = {
//             radius: 5,
//             fillColor: "#FF0000",
//             color: "#000",
//             weight: 1,
//             opacity: 1,
//             fillOpacity: 0.8
//         };
//
//         sink_saline_polygon=L.geoJson(data,geojsonMarkerOptions);
// });
var geojsonLineOptions = {

                color: 'black',
                weight: 2,
                opacity: .7,
                dashArray: '20,15',
                lineJoin: 'round'
    };
        var ut_candidate_network;
        $.getJSON('/static/Data/UT_Network.json',function (data) {


            ut_candidate_network=L.geoJson(data,geojsonLineOptions);



    });
        var albert_candidate_network;
        $.getJSON('/static/Data/Alberta_BaseNetwork.json',function (data) {


            albert_candidate_network=L.geoJson(data,geojsonLineOptions);



    });
        var illinios_candidate_network;
        $.getJSON('/static/Data/Illinois_BaseNetwork.json',function (data) {


            illinios_candidate_network=L.geoJson(data,geojsonLineOptions);



    });

        var ordos_candidate_network;
        $.getJSON('/static/Data/Ordos_Basin_Network.json',function (data) {


            ordos_candidate_network=L.geoJson(data,geojsonLineOptions);



    });

        var se_candidate_network;
        $.getJSON('/static/Data/SoutheastUS_Network.json',function (data) {


            se_candidate_network=L.geoJson(data,geojsonLineOptions);



    });
         var ne_cadidate_network;
        $.getJSON('/static/Data/NE_Network.json',function (data) {


            ne_candidate_network=L.geoJson(data,geojsonLineOptions);


    });

        var sink_coal_layer = L.tileLayer.wms("http://gf8.ucs.indiana.edu/geoserver/SimCCS/wms?", {
                layers: 'SimCCS:NATCARB_Coal',
                format: 'image/png',
                transparent: true
        });

        var sink_oil_layer=L.tileLayer.wms("http://gf8.ucs.indiana.edu/geoserver/SimCCS/wms?", {
                layers: 'SimCCS:NATCARB_OG',
                format: 'image/png',
                transparent: true
        });

        var sink_saline_layer=L.tileLayer.wms("http://gf8.ucs.indiana.edu/geoserver/SimCCS/wms?", {
                layers: 'SimCCS:NATCARB_SALINE',
                format: 'image/png',
                transparent: true
        });

        var sink_ordos_layer=L.tileLayer.wms("http://gf8.ucs.indiana.edu/geoserver/SimCCS/wms?", {
                layers: 'SimCCS:China_OG',
                format: 'image/png',
                transparent: true
        });












