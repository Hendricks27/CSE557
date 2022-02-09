

var zoom_level = 1;
var real_time = 7 * 24 * 3600 + 12*3600;


// each time goes 30s virtually
var update_interval_inside = 30
// update every 100ms
var update_interval_outside = 100
// display now, 10s before and 10s later
var tri_dot_time = 10



var colors = [
    '#ccdd22', '#ff4422','#9911bb','#00bbdd',
    '#3344bb','#828080','#00aaff', '#775544',
    '#ee1166','#44bb44','#88cc44','#009988',
    '#ffee11','#6633bb','#ff9900','#1199ff',
    '#ffcc00','#999999','#ff5500','#444']

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

const main_street = [
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

const st_name_rotate = ["Parla", "Pilau", "Spetson", "Taxiarchon", "", "", ""]
var st_name_counter = {}

var employee_department = {
    'IT': ['1', '5', '6', '8', '17'],
    'Engineering': ['2', '3', '7', '9', '11', '14', '18', '19', '25', '26', '27', '28', '33'],
    'Executive': ['4', '10', '31', '32', '35'],
    'Security': ['12', '13', '15', '16', '20', '21', '22', '23', '24', '30', '34'],
    'Facilities': ['29'],
    'Trucks': [101, 104, 105, 106, 107]
};


var day_filtered_start = 3;
var day_filtered_end = 3;
var second_filter_start = 13*3600;
var second_filter_end   = 16*3600;
var pids_filtered = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
var pids_all = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 101, 104, 105, 106, 107];
var pids_color = {}

var refreshIntervalId = undefined;



const svg = d3.select('#svg1')
    .attr("viewBox", "0 0 135 100")
    .attr("transform", "scale(1.0, -1.0) translate(0,0)")
    .attr('width',  "100%")
    .attr('height', "100%")
    .attr('overflow', "hidden")

const map_g = svg.append("g");
const mapd_g = svg.append("g");
const dot_g = svg.append("g");
const rtd_g = svg.append("g");
const plc_g = svg.append("g");
const home_g = svg.append("g");
const clock_g = svg.append("g");
const time_g = svg.append("g");


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

function is_main_street(n, t){
    for (let pair of main_street){
        if (n == pair[0] && t == pair[1]){
            return true
        }
    }
    return false
}

d3.tsv("./data_map.tsv",
    function (d){
        d.coords = JSON.parse(d.coords);
        var street_width = 0.2;
        var street_color = "white";
        if (is_main_street(d.FENAME, d.FETYPE)){
            street_width = street_width * 4;
            street_color = "RGB(247, 223, 136)";

            if (!Object.keys(st_name_counter).includes(d.FENAME)){st_name_counter[d.FENAME] = 0}
            st_name_counter[d.FENAME] += 1

            var r = "";
            if (st_name_rotate.includes(d.FENAME)){
                r = " rotate(-90)"
            }

            if (st_name_counter[d.FENAME] % 5 == 2){
                mapd_g.append("text")
                .text(d.FENAME + " " + d.FETYPE)
                .style("fill", "grey")
                .attr("transform", "translate("+(coordinate_conversion_long(d.coords[0][0]))+", "+coordinate_conversion_lat(d.coords[0][1]-0.00012)+") scale(0.04, -0.04)" + r)

            }

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



function geo_line(path){
    mapd_g.append("path")
        .datum(path)
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("stroke-width", 0.4)
        .attr("d", d3.line()
            .x(function(coord) {return coordinate_conversion_long(coord[0])})
            .y(function(coord) {return coordinate_conversion_lat(coord[1])})
        )
}

// Long - X-axis - 1km
geo_line([[24.823, 36.0425], [24.914, 36.0425]])
geo_line([[24.9, 36.075], [24.9+0.1/8.99, 36.075]])
geo_line([[24.9, 36.0749], [24.9, 36.076]])
geo_line([[24.911, 36.0749], [24.911, 36.076]])

// Lat - Y-axis
geo_line([[24.823, 36.0424], [24.823, 36.096]])
// Lat 1km geo_line([[24.9, 36.075], [24.9, 36.075+0.06/6.66]])



mapd_g.append("text")
    .text("1 KM")
    .attr("transform", "translate("+(coordinate_conversion_long(24.904))+", "+coordinate_conversion_lat(36.076)+") scale(0.1, -0.1)")

for (var i of [1,2,3,4,5,6,7,8,9]){
    var x = 24.82 + 0.01*i;
    geo_line([[x, 36.0425], [x, 36.0430]])

    var xx = coordinate_conversion_long(x)-2
    var yy = coordinate_conversion_lat(36.0425) - 2.5;
    mapd_g.append("text")
        .text(x.toFixed(2))
        .attr("transform", "translate("+xx+", "+yy+") scale(0.1, -0.1)")
}
for (var i of [1,2,3,4,5]){
    var y = 36.04 + 0.01*i;
    geo_line([[24.823, y], [24.8236, y]])

    var xx = coordinate_conversion_long(24.823) - 3
    var yy = coordinate_conversion_lat(y) + 0.3;
    mapd_g.append("text")
        .text("36.")
        .attr("transform", "translate("+xx+", "+yy+") scale(0.1, -0.1)")

    xx = coordinate_conversion_long(24.823) - 3
    yy = coordinate_conversion_lat(y) - 1.4;
    mapd_g.append("text")
        .text("0"+(i+4).toString())
        .attr("transform", "translate("+xx+", "+yy+") scale(0.1, -0.1)")
}



var location_data = {};
d3.tsv("./data_loc.tsv",
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



function start(){
    var d = document.getElementById("days").value;
    day_filtered_start = parseInt(d);

    var d = document.getElementById("daye").value;
    day_filtered_end = parseInt(d);

    var d = document.getElementById("hours").value;
    second_filter_start = parseInt(d) * 3600;

    var d = document.getElementById("houre").value;
    second_filter_end = parseInt(d) * 3600;

    pids_color = {};
    real_time = day_filtered_start*24*3600 + second_filter_start

    draw_route();

    document.getElementById("start").style.visibility = "hidden"
    document.getElementById("rewind").style.visibility = "visible"
    document.getElementById("play").style.visibility = "visible"
    document.getElementById("forward").style.visibility = "visible"
}


function reset_person_filter_bg_color(){
    for (var pid of pids_all){
        var ele = document.getElementById("pid_name_label_" + pid.toString())
        var rgbc = hexToRgb(pids_color[pid])
        if (rgbc == null ){
            continue
        }
        var rgba = "rgba(" + rgbc.r + "," + rgbc.g + "," + rgbc.b + ",0)"
        ele.style.backgroundColor = rgba
    }
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


    reset_person_filter_bg_color()
    draw_homes()
    table_color_update()
    draw_location_series()
}

function curve(d){
    if (d < 0.01) {
        return 1.1
    }
    return 0.1/d + 0.1
}

function draw_location_series(){

    draw_location()
    refreshIntervalId = setInterval(draw_next_location, update_interval_outside)

    document.getElementById("play").innerHTML = "&nbsp&nbsp&nbsp&nbsp&nbsp\<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"30\" height=\"30\" fill=\"currentColor\" class=\"bi bi-pause\" viewBox=\"0 0 16 16\">\n" +
        "  <path d=\"M6 3.5a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0V4a.5.5 0 0 1 .5-.5zm4 0a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0V4a.5.5 0 0 1 .5-.5z\"/>\n" +
        "</svg>"
}

function draw_next_location(){
    real_time += update_interval_inside;

    if (real_time > day_filtered_end*24*3600 + second_filter_end){
        draw_next_location_pause()
    }
    draw_location()
}

function draw_next_location_pause(){
    clearInterval(refreshIntervalId);
    refreshIntervalId = undefined;

    document.getElementById("play").innerHTML = "                    &nbsp&nbsp&nbsp&nbsp&nbsp\n" +
        "                    <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"30\" height=\"30\" fill=\"currentColor\" class=\"bi bi-play\" viewBox=\"0 0 16 16\">\n" +
        "                      <path d=\"M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z\"/>\n" +
        "                    </svg>"
}


function jump_and_pause(n){
    if (refreshIntervalId != undefined){
        draw_next_location_pause();
    }

    real_time += 3600 * n;
    draw_location();

}

function play_and_pause(){
    if (refreshIntervalId != undefined){
        draw_next_location_pause();
    }
    else{
        draw_location_series();
    }
}



function draw_location(){

    var ts_range = tri_dot_time;
    var valid = false;

    rtd_g.html("");

    clock();
    reset_person_filter_bg_color();


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

            var eleBackground = document.getElementById("pid_name_label_" + pid.toString());
            var rgbc = hexToRgb(pids_color[pid])
            if (rgbc != null){
                var rgba = "rgba(" + rgbc.r + "," + rgbc.g + "," + rgbc.b + ",0.7)"
                eleBackground.style.backgroundColor = rgba
            }

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


    }

    // log()

}


draw_homes();
function draw_homes(){
    home_g.html("");
    d3.tsv("./data_home.tsv",
        function (d){
            var x = coordinate_conversion_long(d.long)
            var y = coordinate_conversion_lat(d.lat)

            var color = "black";
            if (Object.keys(pids_color).includes(d.id)){
                color = pids_color[d.id];
            }

            var xxx = home_g.append("g")
                .attr("transform", "translate("+x+", "+y+") scale(0.10, -0.10)");
            xxx.append("path")
                .attr("stroke", color)
                .attr("transform", "")
                .attr("d", "M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z")
            xxx.append("path")
                .attr("stroke", color)
                .attr("transform", "")
                .attr("d", "M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z")
            xxx.append("text")
                .attr("transform", "translate(5, 12) scale(0.4, 0.4)")
                .text(d.id)
        }
    )
}




draw_places();
function draw_places(){
    plc_g.html("");
    d3.tsv("./data_place.tsv",
        function (d){
            var x = coordinate_conversion_long(d.long)
            var y = coordinate_conversion_lat(d.lat)

            var color = "black";

            var xxx = plc_g.append("g").attr("transform", "translate("+x+", "+y+") scale(0.1, -0.1)")
            xxx.append("path")
                .attr("stroke", "black")
                .attr("transform", "")
                .attr("opacity", "0.4")
                .attr("d", "M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z")
            xxx.append("path")
                .attr("stroke", "black")
                .attr("transform", "")
                .attr("opacity", "0.4")
                .attr("d", "M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z")

            var x_off = 0
            var y_off = 25
            x_off = 0 - d.name.length * 1

            xxx.append("text")
                .attr("transform", "translate("+x_off+", "+y_off+") scale(0.4, 0.4)")
                .text(d.name)
        }
    )
}

fill_table()
d3.csv("./data_people.csv",

    function (d){
        var ele = document.getElementById("pid_name_label_" + d.CarID.toString());
        ele.innerText = d.FirstName + " " + d.LastName
        ele.title = d.CurrentEmploymentTitle
    }

)

function fill_table(){
    var table_div = document.getElementById("kronos_people");
    var table = document.createElement("table");

    for (var dep of Object.keys(employee_department)){
        var tr = document.createElement("tr");
        tr.innerHTML = "<td></td><td></td><td><b>"+dep+":</b></td>"
        table.appendChild(tr)

        var dep_pids = employee_department[dep];
        for (var i in dep_pids){
            var pid = dep_pids[i]

            if (i % 2 == 0){
                var tr = document.createElement("tr");
            }

            var td1 = document.createElement("td");
            var td2 = document.createElement("td");
            var td3 = document.createElement("td");

            var check = document.createElement("input");
            if (pids_filtered.includes(parseInt(pid))){
                check.checked = true
            }
            check.id = "checkbox_" + pid.toString()
            check.type = "checkbox";
            check.onclick = update_pid;

            var tmp = document.createElement("div");
            tmp.id = "color_label_" + pid.toString()
            tmp.style = "width: 10px; height: 10px; background-color: black";

            td3.innerText = pid;
            td3.id = "pid_name_label_" + pid.toString()

            td1.appendChild(check);
            td2.appendChild(tmp);

            tr.appendChild(td1)
            tr.appendChild(td2)
            tr.appendChild(td3)

            table.appendChild(tr)
        }

    }
    table_div.appendChild(table)

}


function table_color_update(){
    for (var pid of pids_all){
        var x = document.getElementById("color_label_" + pid.toString());
        if (Object.keys(pids_color).includes(pid.toString())){
            x.style.backgroundColor = pids_color[pid]
        }
        else{
            x.style.backgroundColor = "white"
        }

    }
}

function update_pid(){
    pids_filtered = [];
    for (var pid of pids_all){
        console.log(pid)
        var x = document.getElementById("checkbox_" + pid.toString());
        if (x.checked){
            pids_filtered.push(pid)
        }

    }
}


function get_date(){
    return parseInt(real_time /(24*3600)) + 8
}

function get_hour(){
    return parseInt((real_time % (24*3600)) / 3600);
}

function get_minute(){
    return parseInt((real_time % 3600) / 60);
}

function log(){
    var ele = document.getElementById("logger");
    var s = "";
    ele.innerText = s;
}


function clock(){
    clock_g.html("")

    var s = "";

    var todayts = real_time % (24*3600);
    var today = parseInt(real_time /(24*3600));

    var h = parseInt(todayts / 3600);
    var m = parseInt((todayts % 3600) / 60);

    s += "1/" + get_date().toString() + "/2014 " + get_hour().toString() +":"+ get_minute().toString()

    clock_g.append("text")
        .attr("transform", "translate(80, 80) scale(0.4, -0.4)")
        .text(s)

}
















// TODO rubbish code
/*
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

 */
