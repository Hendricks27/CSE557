

var zoom_level = 1;
var real_time = 7 * 24 * 3600 + 12*3600;


const svg = d3.select('#svg1')
    .attr("viewBox", "0 0 135 100")
    .attr("transform", "scale(1.05, -1.05) translate(0,0)")
    .attr('width',  1350)
    .attr('height', 1000)
    .attr('overflow', "hidden")


const map_g = svg.append("g");
const dot_g = svg.append("g");
const rtd_g = svg.append("g");
const plc_g = svg.append("g");


var colors = [
    '#ccdd22', '#ff4422','#9911bb','#00bbdd',
    '#3344bb','#828080','#00aaff', '#775544',
    '#ee1166','#44bb44','#88cc44','#009988',
    '#ffee11','#6633bb','#ff9900','#1199ff',
    '#ffcc00','#999999','#ff5500','#444']


function focus(x, y, ratio){
    zoom_level = ratio
    var ts = "scale(" + ratio.toString() + ", -"  + ratio.toString() + ") "+
        "translate(-" + x.toString() + ", -"  + y.toString() + ")"
    svg.attr("transform", ts)
}


// 24.82401 24.91000
// 36.04502 36.09492
function coordinate_conversion_long(x){
    // 24.82 - 24.92 // 0.1 / 8.99km
    // 0 - 100
    let res = (x-24.82) * (100/0.1) * (8.99/6.66)
    return res
}
function coordinate_conversion_lat(y){
    // 36.04 - 36.1 // 0.06 // 6.66km
    // 0 - 100
    let res = (y-36.04)*(100/0.06)
    return res
}

function coordinate_conversion_long_deviate(x, d){
    return coordinate_conversion_long(x) + d
}
function coordinate_conversion_lat_deviate(y, d){
    return coordinate_conversion_lat(y) + d
}


var main_street = [
    ["Parla", "St"],
    ["Pilau", "St"],
    ["Spetson", "St"],
    ["Carnero", "St"],
    ["Barwyn", "St"],
    ["Arkadiou", "St"],
    ["Ermou", "St"],
    ["Androutsou", "St"],
    ["Alfiou", "St"],
    ["Egeou", "Ave"],
    ["Ipsilantou", "Ave"],
    ["Taxiarchon", "Ave"],
    ["Rist", "Way"],
    ["Velestinou", "Blvd"],
    ["", ""],
    ["", ""]
];

function is_main_street(n, t){
    for (let pair of main_street){
        if (n == pair[0] && t == pair[1]){
            return true
        }
    }
    return false
}

d3.tsv("./map.tsv",
    function (d){
        d.coords = JSON.parse(d.coords);
        var street_width = 0.2;
        var street_color = "white";
        if (is_main_street(d.FENAME, d.FETYPE)){
            street_width = street_width * 4;
            street_color = "RGB(247, 223, 136)";
        }
        map_g.append("path")
            .datum(d.coords)
            .attr("fill", "none")
            .attr("stroke", street_color)
            .attr("stroke-width", street_width)
            .attr("d", d3.line()
                .x(function(coords) {
                    return coordinate_conversion_long(coords[0])
                })
                .y(function(coords) {
                    return coordinate_conversion_lat(coords[1])
                })
            )
    },

)
//width="16" height="16" fill="currentColor" class="bi bi-hospital" viewBox="0 0 16 16">

var landscape_data = {}
plc_g.append("g")
    .attr("transform", "translate(50, 30) scale(0.2, -0.2)")
    .append("path")
    .attr("stroke", "black")
    .attr("transform", "")
    .attr("d", "M5 1a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1a1 1 0 0 1 1 1v4h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1h3V3a1 1 0 0 1 1-1V1Zm2 14h2v-3H7v3Zm3 0v-3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v3H5V3h6v12h-1Zm0-14v1H6V1h4Zm2 7v7h3V8h-3Zm-8 7V8H1v7h3Zm4.5-9.966v1.1l.52-.3.433-.25.5.867-.433.25L9 7l.52.3.433.25-.5.866-.433-.25-.52-.3v1.1h-1v-1.1l-.52.3-.433.25-.5-.866.433-.25L7 7l-.52-.3-.433-.25.5-.866.433.25.52.3v-1.1h1ZM2.25 9a.25.25 0 0 0-.25.25v.5c0 .138.112.25.25.25h.5A.25.25 0 0 0 3 9.75v-.5A.25.25 0 0 0 2.75 9h-.5Zm0 2a.25.25 0 0 0-.25.25v.5c0 .138.112.25.25.25h.5a.25.25 0 0 0 .25-.25v-.5a.25.25 0 0 0-.25-.25h-.5ZM2 13.25a.25.25 0 0 1 .25-.25h.5a.25.25 0 0 1 .25.25v.5a.25.25 0 0 1-.25.25h-.5a.25.25 0 0 1-.25-.25v-.5ZM13.25 9a.25.25 0 0 0-.25.25v.5c0 .138.112.25.25.25h.5a.25.25 0 0 0 .25-.25v-.5a.25.25 0 0 0-.25-.25h-.5ZM13 11.25a.25.25 0 0 1 .25-.25h.5a.25.25 0 0 1 .25.25v.5a.25.25 0 0 1-.25.25h-.5a.25.25 0 0 1-.25-.25v-.5Zm.25 1.75a.25.25 0 0 0-.25.25v.5c0 .138.112.25.25.25h.5a.25.25 0 0 0 .25-.25v-.5a.25.25 0 0 0-.25-.25h-.5Z>")

var xxx = plc_g.append("g").attr("transform", "translate(60, 40) scale(0.2, -0.2)");
xxx.append("path")
    .attr("stroke", "black")
    .attr("transform", "")
    .attr("d", "M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z")
xxx.append("path")
    .attr("stroke", "black")
    .attr("transform", "")
    .attr("d", "M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z")




// TODO rubbish code
let x = [[0,0], [100, 100]]
svg.append("path")
    .datum(x)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1)
    .attr("d", d3.line()
        .x(function(coord) {
            return coord[0]
        })
        .y(function(coord) {
            return coord[1]
        })
    )





var location_data = {};
d3.tsv("./loc.tsv",
    function (d){
        if (!Object.keys(location_data).includes(d.pid)){
            location_data[d.pid] = [];
        }

        d.day = parseInt(d.day)
        d.second = parseInt(d.second)

        d.lat = parseFloat(d.lat)
        d.long = parseFloat(d.long)

        // d.evidence = JSON.parse(d.evidence)
        location_data[d.pid].push(d)
    }
)


var day_filtered_start = 3;
var day_filtered_end = 3;
var second_filter_start = 13*3600;
var second_filter_end   = 16*3600;
var pids_filtered = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16];
var pids_color = {}



function refresh(){
    var d = document.getElementById("days").value;
    day_filtered_start = parseInt(d);

    var d = document.getElementById("daye").value;
    day_filtered_end = parseInt(d);

    var d = document.getElementById("hours").value;
    second_filter_start = parseInt(d) * 3600;

    var d = document.getElementById("houre").value;
    second_filter_end = parseInt(d) * 3600;

    // pids_filtered = Object.keys(location_data);
    pids_color = {};
    real_time = (day_filtered_start + 0.5)*24*3600
    draw_route();
}

function draw_route(){

    dot_g.html("");
    var colorindex = 0;

    var diviate = -0.5
    var diviate_step = 1 / pids_filtered.length

    var valid = false;
    for (var pid of pids_filtered){
        if (!Object.keys(location_data).includes(pid)){
            // continue
        }

        for (var dp of location_data[pid]){
            if (dp.day > day_filtered_end){
                continue
            }
            if (dp.day < day_filtered_start){
                continue
            }

            if (dp.day == day_filtered_end && dp.second > second_filter_end){
                continue
            }

            if (dp.day == day_filtered_start && dp.second < second_filter_start){
                continue
            }

            valid = true;
            pids_color[pid] = colors[colorindex]
            dot_g.append("circle")
                .style("stroke", "none")
                .style("fill", pids_color[pid])
                .attr("r", 0.06 + diviate_step * 0.5)
                .attr("cx", coordinate_conversion_long_deviate(dp.long, diviate))
                .attr("cy", coordinate_conversion_lat_deviate(dp.lat, diviate));
        }

        if (valid){
            colorindex += 1
            diviate += diviate_step
        }


    }

    draw_location_series()
}

function curve(d){
    if (d < 0.01) {
        return 1.1
    }
    return 0.1/d + 0.1
}

function draw_location_series(){

    draw_location(10)
    setInterval(draw_next_location, 100, 10)
}

function draw_next_location(t){
    real_time += t;
    draw_location(t)
}

function draw_location(x){

    var ts_range = x;
    var valid = false;
    var colorindex = 0;

    rtd_g.html("");

    for (var pid of pids_filtered){
        if (!Object.keys(location_data).includes(pid)){
            // continue
        }

        var pre_loc = undefined;
        var cur_loc = undefined;
        var fut_loc = undefined;

        for (var dp of location_data[pid]){

            var this_dp_ts = dp.day * 24 * 3600 + dp.second;

            var diff = Math.abs(this_dp_ts - real_time);
            if (diff > ts_range){
                continue
            }
            diff = (this_dp_ts - real_time) / ts_range

            if (pre_loc == undefined){pre_loc = [dp.long, dp.lat, diff]}
            if (cur_loc == undefined){cur_loc = [dp.long, dp.lat, diff]}
            if (fut_loc == undefined){fut_loc = [dp.long, dp.lat, diff]}

            if (Math.abs(diff) < Math.abs(cur_loc[2])){cur_loc = [dp.long, dp.lat, diff]}

            if (diff < pre_loc[2]){pre_loc = [dp.long, dp.lat, diff]}
            if (diff > fut_loc[2]){fut_loc = [dp.long, dp.lat, diff]}


            valid = true;


        }

        if (pre_loc != undefined){
            rtd_g.append("circle")
                .style("stroke", "none")
                .style("opacity", 0.5)
                .style("fill", pids_color[pid])
                .attr("r", 0.6)
                .attr("cx", coordinate_conversion_long(pre_loc[0]))
                .attr("cy", coordinate_conversion_lat(pre_loc[1]));
        }


        if (cur_loc != undefined){
            rtd_g.append("circle")
                .style("stroke", "none")
                .style("opacity", 0.7)
                .style("fill", pids_color[pid])
                .attr("r", 0.85)
                .attr("cx", coordinate_conversion_long(cur_loc[0]))
                .attr("cy", coordinate_conversion_lat(cur_loc[1]));
        }

        if (fut_loc != undefined){
            rtd_g.append("circle")
                .style("stroke", "none")
                .style("opacity", 1)
                .style("fill", pids_color[pid])
                .attr("r", 1)
                .attr("cx", coordinate_conversion_long(fut_loc[0]))
                .attr("cy", coordinate_conversion_lat(fut_loc[1]));
        }





        if (valid){
            colorindex += 1
        }


    }

}

















