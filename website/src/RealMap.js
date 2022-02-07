import React from 'react';
import mapboxgl from 'mapbox-gl';

class RealMap extends React.Component {
componentDidMount() {
// initialize
// Used materials from CSE400E, only MapBox part. The other relevant details will be implemented with MapBox.
let mapStyle = {
    'version': 8,
    'sources': {
        'overlay': {
            'type': 'image',
            'url': `http://localhost:5500/assets/MC2-tourist.jpg`,
            'coordinates': [
                [24.824011, 36.094918],
                [24.909965, 36.094918],
                [24.909965, 36.045015],
                [24.824011, 36.045015],
            ]
        },
    },
    'layers': [
        {
        id: 'background',
        type: 'background',
        paint: {'background-color': 'gray'}
        },
        {
        id: 'overlay',
        source: 'overlay',
        type: 'raster',
        paint: {'raster-opacity': 0.85}
    },]
};

mapboxgl.accessToken = 'pk.eyJ1IjoiYXVyZWxpdXNqciIsImEiOiJja3pibnY0MGwyZzAxMm9tejdpd2xpNGhqIn0.U8GPBQVs-6Al-SppoxZQTw';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    zoom: 13.25, // starting zoom
    style: mapStyle, // style URL
    center: [24.866988, 36.0699665], // starting position [lng, lat]
    minZoom: 10,
    maxZoom: 15,
    maxBounds: new mapboxgl.LngLatBounds([24.80, 36.04], [25.11, 36.10]),
    trackResize: true,
});

// end of initialization
}

render() {
    return (
<div>
<div id='map' style={{width: '1000px', height: '592px'}}>
                    
</div>
</div>
    );
}
}

export default RealMap;


