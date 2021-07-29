$(document).ready(function () {
    if (!no_data){
        soilWaterGauge();
        renderHighchart();
    }

    $('body').on('change', '#farms', function () {
        url = $('#dash').attr('data-cropping-url');
        farmId = $('#farms').val();

        $.ajax({
            url: url,
            data: {
                'farm': farmId,
            },
            success: function (data) {
                $('#croppingholder').html(data);
                $('#cropping').val($("#cropping option:first").val()).trigger('change');
            }
        });
    });
    $('body').on('change', '#cropping', function () {
        url = window.location.href;
        $("#dash").submit()
    });
});

/*  Render the meter gauge in the
    soil water status card in the dashboard */
function soilWaterGauge() {
    var Needle, arc, arcEndRad, arcStartRad, barWidth, chart, chartInset, degToRad, el, endPadRad, height, i, margin, needle, numSections, padRad, percToDeg, percToRad, percent, radius, ref, sectionIndx, sectionPerc, startPadRad, svg, totalPercent, width, subIndicator, label;


    currentpercentMCdec = $("#currentpercentMCdec").val();
    percentPWP = $("#percentPWP").val();
    percentMAD = $("#percentMAD").val();


    if (currentpercentMCdec > 1) {
        currentpercentMCdec = 1;
    }
    else if (currentpercentMCdec < 0) {
        currentpercentMCdec = 0;
    }
    percent = currentpercentMCdec;

    barWidth = 60;

    numSections = 3;

    // / 2 for HALF circle
    //sectionPerc = [(percentPWP - 0.5), (percentMAD - 0.5), (0.5 - (percentPWP - 0.5) - (percentMAD - 0.5))];
    sectionPerc = [(0.5 * percentPWP), ((0.5 * percentMAD) - (0.5 * percentPWP)), (0.5 - (0.5 * percentMAD))];

    padRad = 0;

    chartInset = 10;

    // start at 270deg
    totalPercent = .75;

    subIndicator = totalPercent + (percentMAD * 100 / 200)

    d3.select('#soilwatergauge').remove();
    el = d3.select('.chart-gauge');

    margin = {
        top: 10,
        right: 20,
        bottom: 30,
        left: 20
    };


    width = el[0][0].offsetWidth - margin.left - margin.right;

    height = width;

    radius = Math.min(width, height) / 2;

    percToDeg = function (perc) {
        return perc * 360;
    };

    percToRad = function (perc) {
        return degToRad(percToDeg(perc));
    };

    degToRad = function (deg) {
        return deg * Math.PI / 180;
    };

    svg = el.append('svg').attr('id', 'soilwatergauge').attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom);

    chart = svg.append('g').attr('transform', `translate(${(width + margin.left) / 2}, ${(height + margin.top) / 2})`);

    // build gauge bg
    for (sectionIndx = i = 1, ref = numSections; 1 <= ref ? i <= ref : i >= ref; sectionIndx = 1 <= ref ? ++i : --i) {
        arcStartRad = percToRad(totalPercent);
        arcEndRad = arcStartRad + percToRad(sectionPerc[sectionIndx - 1]);
        totalPercent += sectionPerc[sectionIndx - 1];
        startPadRad = 0;
        endPadRad = 0;
        arc = d3.svg.arc().outerRadius(radius - chartInset).innerRadius(radius - chartInset - barWidth).startAngle(arcStartRad + startPadRad).endAngle(arcEndRad - endPadRad);
        chart.append('path').attr('class', `arc chart-color${sectionIndx}`).attr('d', arc);
    }

    arc2 = d3.svg.arc().outerRadius(radius - chartInset + 10).innerRadius(radius - chartInset - barWidth - 10).startAngle(percToRad(subIndicator)).endAngle(percToRad(subIndicator));
    chart.append('path').attr('d', arc2).style("stroke", "black").style("stroke-width", "2px");

    Needle = class Needle {
        constructor(len, radius1) {
            this.len = len;
            this.radius = radius1;
        }

        drawOn(el, perc) {
            el.append('circle').attr('class', 'needle-center').attr('cx', 0).attr('cy', 0).attr('r', this.radius);
            return el.append('path').attr('class', 'needle').attr('d', this.mkCmd(perc));
        }

        animateOn(el, perc) {
            var self;
            self = this;
            return el.transition().delay(500).ease('elastic').duration(3000).selectAll('.needle').tween('progress', function () {
                return function (percentOfPercent) {
                    var progress;
                    progress = percentOfPercent * perc;
                    return d3.select(this).attr('d', self.mkCmd(progress));
                };
            });
        }

        mkCmd(perc) {
            var centerX, centerY, leftX, leftY, rightX, rightY, thetaRad, topX, topY;
            thetaRad = percToRad(perc / 2); // half circle
            centerX = 0;
            centerY = 0;
            topX = centerX - this.len * Math.cos(thetaRad);
            topY = centerY - this.len * Math.sin(thetaRad);
            leftX = centerX - this.radius * Math.cos(thetaRad - Math.PI / 2);
            leftY = centerY - this.radius * Math.sin(thetaRad - Math.PI / 2);
            rightX = centerX - this.radius * Math.cos(thetaRad + Math.PI / 2);
            rightY = centerY - this.radius * Math.sin(thetaRad + Math.PI / 2);
            return `M ${leftX} ${leftY} L ${topX} ${topY} L ${rightX} ${rightY}`;
        }
    };


    needle = new Needle(65, 10);

    needle.drawOn(chart, 0);

    needle.animateOn(chart, percent);

}

/* Render the highcharts in the dashboard */
function renderHighchart() {
    var soilwater_title = "Soil Water Condition";
    var appliedwater_title = "Applied Water";
    var xrange_title = "Growth Stages";
    var et_title = "Evapotranspiration";

    var chart1;
    var chart2;
    var chart3;

    var hasPlotBand = false;
    
    var date_data=[], date_data_init=[], date_data_dev=[], date_data_mid=[], date_data_late=[],actualRAW_chartdata=[], growth_data = [], eto_chartdata=[], actualet_chartdata=[], adjet_chartdata=[], rain_chartdata=[], irrig_chartdata=[], pwp_chartdata=[], mad_chartdata=[], fc_chartdata=[];
    date_harvest = dh;
    valdMAD = vdmad;
    valPWP = vpwp;
    valFC = vfc;
    for (i=0; i<datetime.length; i++){
        date_data[i] = new Date(datetime[i]).getTime();
        date_data_init[i] = new Date(init[i]).getTime();
        date_data_dev[i] = new Date(dev[i]).getTime();
        date_data_mid[i] = new Date(mid[i]).getTime();
        date_data_late[i] = new Date(late[i]).getTime();
        actualRAW_chartdata.push({
            x: date_data[i],
            y: raw[i]
        });
        rain_chartdata.push({
            x: date_data[i],
            y: rain[i]
        });
        irrig_chartdata.push({
            x: date_data[i],
            y: irrig[i]
        });
        eto_chartdata.push({
            x: date_data[i],
            y: eto[i]
        });
        actualet_chartdata.push({
            x: date_data[i],
            y: actet[i]
        });
        adjet_chartdata.push({
            x: date_data[i],
            y: adjet[i]
        });
        pwp_chartdata.push({
            x: date_data[i],
            y: pwp[i]
        });
        mad_chartdata.push({
            x: date_data[i],
            y: mad[i]
        });
        fc_chartdata.push({
            x: date_data[i],
            y: fc[i]
        });
    }
    if (date_data_init != ""){
        growth_data.push({
            x: (date_data_init[0]),
            x2: (date_data_init[date_data_init.length-1]),
            y:0,
            color: "#acd14f",
            stage: "Initial Stage",
        });
        if (date_data_dev != ""){
            growth_data.push({
                x: (date_data_dev[0]),
                x2: (date_data_dev[date_data_dev.length-1]),
                y:0,
                color: "#86d640",
                stage: "Developmental Stage",
            });
            if (date_data_mid != ""){
                growth_data.push({
                    x: (date_data_mid[0]),
                    x2: (date_data_mid[date_data_mid.length-1]),
                    y:0,
                    color: "#40d656",
                    stage: "Mid-season",
                });
                if (date_data_late != ""){
                    growth_data.push({
                        x: (date_data_late[0]),
                        x2: (date_data_late[date_data_late.length-1]),
                        y:0,
                        color: "#1ebd4e",
                        stage: "Late Season",
                    });
                }
            }
        }
    }
    

    //catch mousemove event and have all 3 charts' crosshairs move along indicated values on x axis

    function syncronizeCrossHairs(chart) {
        var container = $(chart.container),
            offset = container.offset(),
            x, y, isInside, report;

        container.mousemove(function (evt) {

            x = evt.clientX - chart.plotLeft - offset.left;
            y = evt.clientY - chart.plotTop - offset.top;
            var xAxis = chart.xAxis[0];
            var xVal = xAxis.toValue(x, true);
            //remove old plot line and draw new plot line (crosshair) for this chart
            var xAxis1 = chart1.xAxis[0];
            var points1 = [chart1.series[0].points, chart1.series[1].points, chart1.series[2].points, chart1.series[3].points];

            Highcharts.each(points1, function (point, i) {
                if (i + 1 < points1.length && point.x <= xVal && points1[i + 1].x > xVal) {
                    if (xVal - point.x <= points1[i + 1].x - xVal) {
                        chart1.tooltip.refresh(point);
                        point.setState('hover');
                    } else {
                        chart1.tooltip.refresh(points1[i + 1]);
                        points1[i + 1].setState('hover');
                    }
                }
            });

            xAxis1.removePlotLine("myPlotLineId");
            xAxis1.addPlotLine({
                value: chart.xAxis[0].translate(x, true),
                width: 1,
                color: 'red',
                id: "myPlotLineId"
            });

            var xAxis2 = chart2.xAxis[0];
            var points2 = [chart2.series[0].points, chart2.series[1].points];
            Highcharts.each(points2, function (point, i) {
                if (i + 1 < points2.length && point.x <= xVal && points2[i + 1].x > xVal) {
                    if (xVal - point.x <= points2[i + 1].x - xVal) {
                        chart2.tooltip.refresh(point);
                        point.setState('hover');
                    } else {
                        chart2.tooltip.refresh(points2[i + 1]);
                        points2[i + 1].setState('hover');
                    }
                }
            });

            xAxis2.removePlotLine("myPlotLineId");
            xAxis2.addPlotLine({
                value: chart.xAxis[0].translate(x, true),
                width: 1,
                color: 'red',
                //dashStyle: 'dash',                   
                id: "myPlotLineId"
            });

            //remove old crosshair and draw new crosshair on chart2
            var xAxis3 = chart3.xAxis[0];
            var points3 = chart3.series[0].points;
            xAxis3.removePlotLine("myPlotLineId");
            xAxis3.addPlotLine({
                value: chart.xAxis[0].translate(x, true),
                width: 1,
                color: 'red',
                id: "myPlotLineId"
            });

            Highcharts.each(points3, function (point) {

                if (point.x < xVal && point.x2 > xVal) {
                    chart3.tooltip.refresh(point);
                    point.update({
                        color: '#4879b2'
                    });
                } else {
                    point.update({
                        color: '#fff'
                    });
                }
            });

            var xAxis4 = chart4.xAxis[0];
            var points4 = [chart4.series[0].points, chart4.series[1].points, chart4.series[2].points];
            Highcharts.each(points4, function (point, i) {
                if (i + 1 < points4.length && point.x <= xVal && points4[i + 1].x > xVal) {
                    if (xVal - point.x <= points4[i + 1].x - xVal) {
                        chart4.tooltip.refresh(point);
                        point.setState('hover');
                    } else {
                        chart4.tooltip.refresh(points4[i + 1]);
                        points4[i + 1].setState('hover');
                    }
                }
            });

            xAxis4.removePlotLine("myPlotLineId");
            xAxis4.addPlotLine({
                value: chart.xAxis[0].translate(x, true),
                width: 1,
                color: 'red',
                //dashStyle: 'dash',                   
                id: "myPlotLineId"
            });

            //if you have other charts that need to be syncronized - update their crosshair (plot line) in the same way in this function.                   
        });
    }

    //Soil Water container
    chart1 = Highcharts.chart('soilwaterChart', {
        chart: {
            type: 'spline',
            marginLeft: 87,
            zoomType: 'x',
            height: 400,
            plotBackgroundColor: {
                linearGradient: [0, 0, 0, 400],
                stops: [
                    [(1 - (Math.min.apply(Math, valdMAD) / Math.min.apply(Math, valFC))), '#856f52'],
                    [(1 - 0.9 * (Math.min.apply(Math, valdMAD) / Math.min.apply(Math, valFC))), '#856f52'],
                    [(1 - 0.8 * (Math.min.apply(Math, valdMAD) / Math.min.apply(Math, valFC))), '#b39369'],
                    [(1 - 0.7 * (Math.min.apply(Math, valdMAD) / Math.min.apply(Math, valFC))), '#b39369'],
                    [(1 - 0.5 * (Math.min.apply(Math, valdMAD) / Math.min.apply(Math, valFC))), '#c9a473'],
                    [(1 - (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#c9a473'],
                    [(1 - 0.9 * (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#e3b87f'],
                    [(1 - 0.8 * (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#e3b87f'],
                    [(1 - 0.7 * (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#c79f69'],
                    [(1 - 0.5 * (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#f7d4a6'],
                    [(1 - 0.2 * (Math.min.apply(Math, valPWP) / Math.min.apply(Math, valFC))), '#f7d4a6'],
                ]
            }
        },


        title: {
            text: soilwater_title,
            align: 'left',
            margin: 10,
            x: 0
        },

        xAxis: {
            //today
            events: {
                afterSetExtremes: function () {
                    var xMin = this.chart.xAxis[0].min;
                    var xMax = this.chart.xAxis[0].max;

                    chart2.xAxis[0].setExtremes(xMin, xMax);
                    chart3.xAxis[0].setExtremes(xMin, xMax);
                }
            },
            plotLines: [{ // mark the weekend
                color: '#9B9B9B',
                width: 1,
                value: new Date(date_harvest).getTime(),
            }],
            type: 'datetime',
            labels: {
                format: '{value:%b %e}'
            },
        },
        yAxis: {
            reversed: false,
            title: {
                text: '',
                max: 100,
                lineWidth: 0, //get rid of the 
                minorGridLineWidth: 0,
                lineColor: 'transparent',
                floor: 0,
                ceiling: 100
            },
            labels: {
                format: '{value} mm'
            },
            gridLineColor: 'transparent',
            min: Math.min.apply(Math, valPWP),
            startOnTick: true,

        },
        series: [{
            name: 'Field Capacity',
            data: fc_chartdata,
            color: '#41d165',
            lineWidth: 3,
        }, {
            name: 'Management Allowable Depletion',
            data: mad_chartdata,
            color: '#ffc629',
            lineWidth: 3,
        }, {
            name: 'Permanent Wilting Point',
            data: pwp_chartdata,
            color: '#ff4229',
            lineWidth: 3,
        }, {
            name: 'Current Soil Moisture Content',
            data: actualRAW_chartdata,
            zones: [{
                value: Math.min.apply(Math, valPWP),
                dashStyle: 'dot'
            }, {
                value: Math.min.apply(Math, valdMAD),
                dashStyle: 'dot'
            }],
            color: {
                linearGradient: [0, 0, 0, 200],
                stops: [
                    [0, 'rgb(99, 206, 255)'],
                    [0.5, 'rgb(168, 235, 204)'],
                    [1, 'rgb(13, 132, 212)']
                ]
            }
        }],
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            },
        },
        credits: {
            enabled: false
        },
    }, function (chart) {
        syncronizeCrossHairs(chart);
    });

    //Applied Water container
    chart2 = Highcharts.chart('appliedwaterChart', {
        chart: {
            type: 'line',
            marginLeft: 87,
            height: 250,
            zoomType: 'x',
        },
        title: {
            text: appliedwater_title,
            align: 'left',
            margin: 10,
            x: 0
        },
        xAxis: {
            //today
            events: {
                afterSetExtremes: function () {
                    var xMin = this.chart.xAxis[0].min;
                    var xMax = this.chart.xAxis[0].max;

                    chart1.xAxis[0].setExtremes(xMin, xMax);
                    chart2.xAxis[0].setExtremes(xMin, xMax);
                }
            },
            plotLines: [{ // mark the weekend
                color: '#9B9B9B',
                width: 1,
                value: new Date(date_harvest).getTime(),
            }],
            type: 'datetime',
            labels: {
                format: '{value:%b %e}'
            },
        },
        yAxis: {
            title: '',
            labels: {
                format: '{value} mm'
            },
        },
        plotOptions: {
            line: {
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 2
                    }
                },
                marker: {
                    enabled: false
                },
            },

        },
        series: [{
            name: 'Rainfall',
            color: '#47ceff',
            data: rain_chartdata,
        }, {
            name: 'Irrigation',
            color: '#8ccc64',
            data: irrig_chartdata,
        }],
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        credits: {
            enabled: false
        },

    }, function (chart) {
        syncronizeCrossHairs(chart);
    });

    //Growth Stage container
    chart3 = new Highcharts.chart('growthstageChart', {
        chart: {
            type: 'xrange',
            zoomType: 'x',
            marginLeft: 87,
            height: 200,
            resetZoomButton: {
                theme: {
                    fill: 'white',
                    stroke: '#4A90E2',
                    color: '#4A90E2',
                    r: 0,
                    states: {
                        hover: {
                            fill: '#4A90E2',
                            style: {
                                color: 'white'
                            }
                        }
                    }
                }
            }
        },
        title: {
            text: xrange_title,
            align: 'left',
            margin: 10,
            x: 0
        },
        xAxis: {
            events: {
                afterSetExtremes: function () {
                    var xMin = this.chart.xAxis[0].min;
                    var xMax = this.chart.xAxis[0].max;

                    chart1.xAxis[0].setExtremes(xMin, xMax);
                    chart3.xAxis[0].setExtremes(xMin, xMax);
                }
            },
            type: 'datetime',
            labels: {
                format: '{value:%b %e}'
            },
            plotLines: [{ // mark the weekend
                color: '#9B9B9B',
                width: 1,
                value: new Date(date_harvest).getTime(),
            }],
        },
        yAxis: {
            categories: ['Stage'],
            title: {
                text: ''
            },
        },
        plotOptions: {
            xrange: {
                pointPlacement: "on"
            }
        },
        series: [{
            name: 'Plant Growth Stage',
            borderColor: '#53c447',
            pointWidth: 18,
            data: growth_data,
            dataLabels: {
                enabled: true,
            },
            maxPointWidth: 20,
        }],
        tooltip: {
            formatter: function () {
                return this.series.name + '<br> <b>' + this.point.stage + '</b>';
            }
        },
        credits: {
            enabled: false
        },
    }, function (chart) {
        syncronizeCrossHairs(chart);
    });

    //Evapotranspiration container
    chart4 = Highcharts.chart('etChart', {
        chart: {
            type: 'line',
            marginLeft: 87,
            height: 300,
            zoomType: 'x',
        },
        title: {
            text: et_title,
            align: 'left',
            margin: 10,
            x: 0
        },
        xAxis: {
            //today
            events: {
                afterSetExtremes: function () {
                    var xMin = this.chart.xAxis[0].min;
                    var xMax = this.chart.xAxis[0].max;

                    chart1.xAxis[0].setExtremes(xMin, xMax);
                    chart2.xAxis[0].setExtremes(xMin, xMax);
                }
            },
            plotLines: [{ // mark the weekend
                color: '#9B9B9B',
                width: 1,
                value: new Date(date_harvest).getTime(),
            }],
            type: 'datetime',
            labels: {
                format: '{value:%b %e}'
            },
        },
        yAxis: {
            title: '',
            labels: {
                format: '{value} mm'
            },
        },
        plotOptions: {
            line: {
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 2
                    }
                },
                marker: {
                    enabled: false
                },
            },

        },
        series: [{
            name: 'Reference ET',
            color: '#4797ff',
            data: eto_chartdata,
        }, {
            name: 'Actual ET',
            color: '#ffb753',
            data: actualet_chartdata,
        }, {
            name: 'Adjusted ETo',
            color: '#53ff9e',
            data: adjet_chartdata,
        }],
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        credits: {
            enabled: false
        },

    }, function (chart) {
        syncronizeCrossHairs(chart);
    });

    (function () {
        var longestW = chart1.plotLeft;
        var charts = [chart4, chart3, chart2, chart1];
        Highcharts.each(charts, function (chart, i) {
            if (i < charts.length - 1 && charts[i].plotLeft < charts[i + 1].plotLeft) {
                longestW = charts[i + 1].plotLeft;
            }
        });
        Highcharts.each(charts, function (chart) {
            chart3.update({
                yAxis: {
                    labels: {
                        padding: 150
                    }
                }
            });
        });
    })();

}
